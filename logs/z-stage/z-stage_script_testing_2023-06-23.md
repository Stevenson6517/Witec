z-stage\_script\_testing\_2023-06-23

Friday, June 23, 2023

2:40 PM

Windows 7 PC (HP)

-   Sent command "echo 1.0 1 nr &gt; COM7" to z-stage via cmd as administrator

    -   "access is denied"

    -   Changed COM7 to COM1 in device manager

        -   Didn't work

    -   Restarted computer

-   Sent command "1.0 1 nr" to pollux via PIMikroMove Command Entry -- didn't work

    -   Closed PIMikroMove -- no error, but no response

-   Sent command "HLP?"

    -   Listed following commands:

> &lt;&lt;\#4 query status word
>
> &lt;&lt;\#5 request motion status
>
> &lt;&lt;\#7 request controller ready status
>
> &lt;&lt;\#24 stop all axes
>
> &lt;&lt;\*IDN? Get Device Identification
>
> &lt;&lt;ACC {&lt;AxisID&gt; &lt;Acceleration&gt;}
>
> &lt;&lt;ACC? \[{&lt;AxisID&gt;}\] get closed-loop acceleration
>
> &lt;&lt;CST {&lt;AxisID&gt; &lt;StageName&gt;} set assignment of stages to axes
>
> &lt;&lt;CST? \[{&lt;AxisID&gt;}\] get assignment of stages to axes
>
> &lt;&lt;CSV? get current syntax version
>
> &lt;&lt;DEC? \[{&lt;AxisID&gt;}\]
>
> &lt;&lt;DFH \[{&lt;AxisID&gt;}\]
>
> &lt;&lt;DFH? \[{&lt;AxisID&gt;}\]
>
> &lt;&lt;ERR? get error number
>
> &lt;&lt;FED &lt;AxisID&gt; &lt;EdgeID&gt; &lt;param&gt;
>
> &lt;&lt;FNL \[{&lt;AxisID&gt;}\]
>
> &lt;&lt;FPL \[{&lt;AxisID&gt;}\]
>
> &lt;&lt;FRF \[{&lt;AxisID&gt;}\] fast reference move to reference switch
>
> &lt;&lt;FRF? \[{&lt;AxisID&gt;}\] get referencing result
>
> &lt;&lt;GOH {&lt;AxisID&gt;}
>
> &lt;&lt;HLP? get list of available commands
>
> &lt;&lt;HLT \[{&lt;AxisID&gt;}\] halt motion smoothly
>
> &lt;&lt;HPA? get list of available parameters
>
> &lt;&lt;IDN? get device identification
>
> &lt;&lt;INI \[{&lt;AxisID&gt;}\] initialize
>
> &lt;&lt;LIM? \[{&lt;AxisID&gt;}\] indicate limit switches
>
> &lt;&lt;MOV {&lt;AxisID&gt; &lt;Position&gt;} set target position (start absolute motion)
>
> &lt;&lt;MOV? \[{&lt;AxisID&gt;}\] get target position
>
> &lt;&lt;MVR {&lt;AxisID&gt; &lt;Distance&gt;} set target relative to current position (start relative motion)
>
> &lt;&lt;ONT? \[{&lt;AxisID&gt;}\] get on-target state
>
> &lt;&lt;POS {&lt;AxisID&gt; &lt;Position&gt;}
>
> &lt;&lt;POS? \[{&lt;AxisID&gt;}\] get real position
>
> &lt;&lt;RBT reboot system
>
> &lt;&lt;RON {&lt;AxisID&gt; &lt;ReferenceOn&gt;}
>
> &lt;&lt;RON? \[{&lt;AxisID&gt;}\] get reference mode
>
> &lt;&lt;SAI {&lt;AxisID\_Old&gt; &lt;AxisID\_New&gt;}
>
> &lt;&lt;SAI? \["ALL"\] get list of current axis identifiers
>
> &lt;&lt;SPA {&lt;ItemID&gt; &lt;PamID&gt; &lt;PamValue&gt;} set volatile memory parameters
>
> &lt;&lt;SPA? \[{&lt;ItemID&gt; &lt;PamID&gt;}\] get volatile memory parameters
>
> &lt;&lt;SRG? &lt;AxisID&gt; &lt;RegisterID&gt;
>
> &lt;&lt;STP stop all axes abruptly
>
> &lt;&lt;SVO {&lt;AxisID&gt; &lt;ServoState&gt;} set servo mode
>
> &lt;&lt;SVO? \[{&lt;AxisID&gt;}\] get servo mode
>
> &lt;&lt;TMN? \[{&lt;AxisID&gt;}\] get minimum commandable position
>
> &lt;&lt;TMX? \[{&lt;AxisID&gt;}\] get maximum commandable position
>
> &lt;&lt;TRS? \[{&lt;AxisID&gt;}\] indicate reference point switch
>
> &lt;&lt;TVI? tell valid character set for axis identifiers
>
> &lt;&lt;VEL {&lt;AxisID&gt; &lt;Velocity&gt;} set closed-loop velocity
>
> &lt;&lt;VEL? \[{&lt;AxisID&gt;}\] get closed-loop velocity
>
> &lt;&lt;VER? get version
>
> &lt;&lt;VST? list available stages
>
> &lt;&lt;WPA &lt;Password&gt; Save Parameters To Non-Volatile Memory

-   Sent command "MVR 1 3" via Command Entry in PIMikroMove -- microscope moved up

<!-- -->

-   PuTTY

    -   Serial connection on COM7, speed 19200, "z-stage" -- does not work

        -   "After you start up PuTTY in serial mode, you might find that you have to make the first move, by sending some data out of the serial line in order to notify the device at the other end that someone is there for it to talk to." -- from the manual

    -   Serial connection does not work on Windows 10 PC either

    -   PLINK immediately closes itself after launch

-   Virtual COMs?

-   Toshiba w/ RS232

    -   Install linux

>  
>
>  
