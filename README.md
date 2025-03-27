# Inline-EA
Inline-EA is a Beacon Object File (BOF) to execute .NET assemblies in your current Beacon process.
This tool was built to bypass the latest Elastic at the time of making, version 8.17.4. This tool also works against CrowdStrike Falcon and Microsoft Defender for Endpoint (MDE).

## Features

- Load necessary CLR DLLs using LoadLibraryShim to evade ICLRRuntimeInfo::GetInterface callstack detections
- Load a console from backed memory by using APCs
- Bypass AMSI by patching clr.dll instead of amsi.dll to avoid common detections
- Bypass ETW by EAT Hooking advapi32.dll!EventWrite to point to a function that returns right away
- Patches System.Environment.Exit to prevent Beacon process from exiting

## Usage

You can compile by going into the `src/` directory and running `x86_64-w64-mingw32-gcc -c main.cpp -o inline-ea.x64.o`.

Put the `inline-ea.cna` Aggressor Script and `inline-ea.x64.o` BOF into the same directory, then load `inline-ea.cna` into your Script Manager.

You can run the help command in your Beacon console with: `help inline-ea`

To run .NET assemblies, use the command: `inline-ea /Path/To/Assembly.exe [arguments...]`

Optionally:
  `--amsi` and `--etw` flags can be used to bypass AMSI and ETW respectively.
  `--patchexit` flag can be used to patch System.Environment.Exit, though this isn't always necessary and it does get detected by Elastic.

```
beacon> help inline-ea
Synopsis: inline-ea /path/to/Assembly.exe [arguments...] [--patchexit] [--amsi] [--etw]
Description:
  Execute a .NET assembly in the current beacon process.

  --patchexit   Optional. Patches System.Environment.Exit (flagged by Elastic).
  --amsi        Optional. Patches AmsiScanBuffer to bypass AMSI.
  --etw         Optional. Patches ETW EventWrite.

Examples:
  inline-ea /path/to/Rubeus.exe triage --amsi --etw --patchexit
  inline-ea /path/to/Powerpick.exe whoami /all --amsi --etw
```

## Demo
View the full demo against all 3 security products on my [website](https://ericesquivel.github.io/posts/inline-ea)

## Resources

* [InlineExecute-Assembly](https://github.com/anthemtotheego/InlineExecute-Assembly) by AnthemToTheEgo - Provided a base template for inline executing .NET assemblies in C in a BOF. I just had to port it from C to C++.
* [Maldev Academy](https://maldevacademy.com) - Contained a great module for inline executing .NET assemblies in C++ as a normal program, but not as a BOF. I combined this and AnthemToTheEgo's project to execute .NET assemblies in C++ as a BOF.
* [Unmanaged .NET Patching](https://kyleavery.com/posts/unmanaged-dotnet-patching) by Kyle Avery - Resource on how to patch System.Environment.Exit.
* [New AMSI Bypass Technique Modifying CLR.DLL in Memory](https://practicalsecurityanalytics.com/new-amsi-bypss-technique-modifying-clr-dll-in-memory) by Practical Security Analytics LLC - Patching clr.dll to bypass AMSI.
* [EAT Hooking](https://www.unknowncheats.me/forum/c-and-c/50426-eat-hooking-dlls.html) by Jimster480 - I came up with the idea to bypass ETW by EAT Hooking advapi32.dll!EventWrite and I found this general EAT Hooking code snippet which worked great.
