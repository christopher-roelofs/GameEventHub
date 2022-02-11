"""

[
                {
                    "MisterCoreChange": [
                        {
                            "description": "custom script on core change",
                            "status": "enabled",
                            "file": "details.txt",
                            "script": "scripts/write_details_kruizcontrol.py",
                            "format":""
                        }
                    ]
                },
                {
                    "MisterGameChange": [
                        {
                            "description": "custom script on game change",
                            "status": "enabled",
                            "file": "details.txt",
                            "script": "scripts/write_details_kruizcontrol.py",
                            "format":"KruizControl"
                        }
                    ]
                }
            ]

"""


def rom_to_kruiz_control(rom):
    content = ""
    if rom == "":
        return ""
    for detail in rom:
        if detail == "release_name":
            if rom["release_name"] !="":
                content = content + "name\n"
                content = content + f'{rom["release_name"]} \n'
        if rom["region"] !="":
            if detail == "region":
                content = content + "region\n"
                content = content + f'{rom["region"]} \n'
        if rom["system"] !="":
            if detail == "system":
                content = content + "system\n"
                content = content + f'{rom["system"]} \n'
        if rom["developer"] !="":
            if detail == "developer":
                content = content + "developer\n"
                content = content + f'{rom["developer"]} \n'
        if rom["publisher"] !="":
            if detail == "publisher":
                content = content + "publisher\n"
                content = content + f'{rom["publisher"]} \n'
        if rom["genre"] !="":
            if detail == "genre":
                content = content + "genre\n"
                content = content + f'{rom["genre"]} \n'
        if rom["date"] !="":
            if detail == "date":
                content = content + "date\n"
                content = content + f'{rom["date"]} \n'
        if rom["description"] !="":
            if detail == "description":
                content = content + "description\n"
                content = content + f'{rom["description"]} \n'
        if rom["reference_url"] !="":
            if detail == "reference_url":
                content = content + "url\n"
                content = content + f'{rom["reference_url"]} \n'
        if rom["manual_url"] !="":
            if detail == "manual_url":
                content = content + "manual\n"
                content = content + f'Manual: {rom["manual_url"]} \n'
    return(content)

def write_to_file(content,filename):
    try:
        with open(filename, 'w') as f:
            f.write(content)
            logger.event(f"Rom details writtent to {filename}")
    except Exception as e:
        logger.error(f"Failed to write content file to {filename}")



if action["format"] == "":
    write_to_file("",action["file"])
if action["format"] == "KruizControl":
    content = rom_to_kruiz_control(event.rom)
    write_to_file(content,action["file"])
