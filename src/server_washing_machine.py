

import asyncio
import logging
import sys
sys.path.insert(0, "..")
from IPython import embed

from asyncua import ua, uamethod, Server
from asyncua.common.instantiate_util import instantiate
from asyncua.common.node import Node



async def main():
    
    logging.basicConfig(level=logging.INFO)
    server = Server()
    await server.init()
    
    # import some nodes from xml
    nodes1 = await server.import_xml("./ims/di.xml")
    nodes2 = await server.import_xml("./ims/washingmachine.xml")

    washing_machine_type = server.get_node("ns=3;i=1002")
    print(washing_machine_type)

    # instatiate as WashingMachine
    washing_machine = await instantiate(server.nodes.objects, washing_machine_type, bname="3:WashingMachine", instantiate_optional=False)
    washing_machine = washing_machine[0]
    print(washing_machine)

    # get all children of washing machine instance and print list
    all_kids = await washing_machine.get_children()
    print(all_kids)

    # get specific childs
    washing_machine_manufacturer = await washing_machine.get_child(["2:Manufacturer"])
    washing_machine_model = await washing_machine.get_child(["2:Model"])
    washing_machine_serial = await washing_machine.get_child(["2:SerialNumber"])


    # starting!
    async with server:
        while True:
            await asyncio.sleep(1)
            await washing_machine_manufacturer.write_value("Muehle")
            await washing_machine_model.write_value("Sauber 3000")
            await washing_machine_serial.write_value("ABC123456789")


if __name__ == "__main__":
    asyncio.run(main())
