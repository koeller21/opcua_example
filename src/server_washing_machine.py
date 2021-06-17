

import asyncio
import logging
import sys
sys.path.insert(0, "..")
from IPython import embed
from datetime import datetime

from asyncua import ua, uamethod, Server
from asyncua.common.instantiate_util import instantiate
from asyncua.common.node import Node


@uamethod
def setMode(parent, mode):
    print("Method call with param: " + str(mode))
    return True


async def main():
    
    logging.basicConfig(level=logging.DEBUG)
    server = Server()
    server.name = "Washing Machine Demo Server"
    

    await server.init()

    # import some nodes from xml
    nodes1 = await server.import_xml("./ims/di.xml")
    nodes2 = await server.import_xml("./ims/washingmachine.xml")

    # washing machine uri
    uri = "http://yourorganisation.org/washingMachine/"
    idx = await server.get_namespace_index(uri)

    # get washing machine type
    washing_machine_type = server.get_node("ns=3;i=1002")

    # instatiate as WashingMachine by adding to objects folder
    # this, internally, calls instantiate
    washing_machine = await server.nodes.objects.add_object(nodeid=idx, bname="WashingMachine", objecttype=washing_machine_type, instantiate_optional=True)

    # get all references of washing machine instance (no use here)
    all_references = await washing_machine.get_references()

    # get all children of washing machine instance 
    all_kids = await washing_machine.get_children()

    # iterate over all children of washing machine instance
    for child in all_kids:
        
        # get brows name of each of them
        browse_name = await child.read_browse_name()

        # if browse_name is subcomponents
        if browse_name.Name == "SubComponents":

            # then delete child of subcomponents as this is a mandatory placeholder
            subcomponent_idf = await child.get_child(["3:SubComponent_Identifier"])
            
            # delete that bad boy
            await subcomponent_idf.delete()


    # get washing machine door type
    washing_machine_door_type = server.get_node("ns=3;i=1003")

    # get the subcomponents type first in the washing machine
    washing_machine_subcomponents = await washing_machine.get_child(["3:SubComponents"])

    # then instantiate the door type
    washing_machine_door = await washing_machine_subcomponents.add_object(nodeid=idx, bname="WashingMachineDoor", objecttype=washing_machine_door_type, instantiate_optional=True)

    # get specific children (properties) for writing
    washing_machine_manufacturer = await washing_machine.get_child(["3:Identification","2:Manufacturer"])
    washing_machine_serial = await washing_machine.get_child(["3:Identification", "2:SerialNumber"])

    await washing_machine_manufacturer.write_value("Muehle")
    await washing_machine_serial.write_value("ABC123456789")

    # load enums from server
    await server.load_enums()

    # get variable child (variable)
    washing_machine_rpm = await washing_machine.get_child(["2:ParameterSet", "3:RPM"])
    washing_machine_currentmode = await washing_machine.get_child(["2:ParameterSet", "3:CurrentMode"])
    washing_machine_door_doorOpened = await washing_machine_door.get_child(["2:ParameterSet", "3:DoorOpened"])


    # link method with callback function
    washing_machine_set_mode_func = await washing_machine.get_child(["2:MethodSet", "3:SetMode"])
    server.link_method(washing_machine_set_mode_func, setMode)



    # starting!
    async with server:
        while True:
            await asyncio.sleep(1)

            # change variable values
            await washing_machine_rpm.write_value(23)
            # use enum from server!
            await washing_machine_currentmode.write_value(ua.WashingMachineStateEnumeration.Normal)
            await washing_machine_door_doorOpened.write_value(False)



if __name__ == "__main__":
    asyncio.run(main())
