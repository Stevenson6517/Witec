z-stage\_script\_2023-06-22

Wednesday, June 22, 2023

6:46 PM

<img src="media/image1.jpeg" style="width:5in;height:5.07639in" />

Fan-out gate will be spliced into cable connecting T-B to Feedback Module. Copied analog voltage will be sent to Arduino, converting it to digital format and sending voltage to Windows computer via USB. If voltage is greater than 0 (or some value), batch script on windows will send stop command to z-stage.

 

(System block diagram attached)

 

**<u>Arduino Code</u>**

\`\`\`

const int analogInputPin = A0; // Analog input pin

const int digitalOutputPin = 13; // Digital output pin

 

const int threshold = 512; // Threshold value for conversion

 

void setup() {

pinMode(digitalOutputPin, OUTPUT); // Set the digital pin as an output

Serial.begin(9600); // Initialize the serial communication (for debugging)

}

 

void loop() {

int analogValue = analogRead(analogInputPin); // Read the analog input voltage

 

if (analogValue &gt;= threshold) {

digitalWrite(digitalOutputPin, HIGH); // Set the digital output pin HIGH

} else {

digitalWrite(digitalOutputPin, LOW); // Set the digital output pin LOW

}

 

Serial.println(analogValue); // Print the analog value (for debugging)

delay(100); // Delay between readings (adjust as needed)

}

\`\`\`

 

Here's how the code works:

 

1\. Define the analog input pin (\`analogInputPin\`) where your voltage signal is connected, and the digital output pin (\`digitalOutputPin\`) where you want the corresponding digital output signal.

 

2\. Set the threshold value (\`threshold\`) that determines the conversion from analog to digital. When the analog value is greater than or equal to the threshold, the digital output pin will be set HIGH; otherwise, it will be set LOW.

 

3\. In the \`setup()\` function, set the \`digitalOutputPin\` as an output using \`pinMode()\`. Also, initialize the serial communication at a baud rate of 9600 for debugging purposes (optional).

 

4\. In the \`loop()\` function, read the analog voltage using \`analogRead(analogInputPin)\` and store it in the \`analogValue\` variable.

 

5\. Check if \`analogValue\` is greater than or equal to the threshold. If it is, set the \`digitalOutputPin\` HIGH using \`digitalWrite()\`. Otherwise, set it LOW.

 

6\. Print the \`analogValue\` to the serial monitor using \`Serial.println()\` for debugging purposes (optional).

 

7\. Add a delay between readings using \`delay()\` to control the sampling rate. Adjust the delay duration as needed.

 

Upload the code to your Arduino board, and the digital output pin (\`digitalOutputPin\`) will reflect the digital representation of the analog input voltage based on the defined threshold.

 

 

**<u>Batch Script</u>**

\`\`\`

@echo off

 

set ArduinoCOMPort=COM3         :: COM port where Arduino is connected

set TargetCOMPort=COM1         :: COM port to send the command

set Threshold=0

 

:loop

for /F "usebackq tokens=2 delims=:" %%a in (\`mode %ArduinoCOMPort% ^| find "Status"\`) do (

set "status=%%a"

)

set status=%status:~1,-1%

 

if %status% GTR %Threshold% (

echo 1 nabort &gt; %TargetCOMPort%

)

 

timeout /t 1 &gt; nul         :: Adjust the timeout duration as needed

goto loop

\`\`\`

 

Here's what has changed:

 

1\. Set the \`ArduinoCOMPort\` variable to the appropriate COM port number where your Arduino is connected.

 

2\. Set the \`TargetCOMPort\` variable to the COM port where you want to send the command. Modify it based on your requirements.

 

3\. The script monitors the status of the \`ArduinoCOMPort\` using the \`mode\` command to extract the status value.

 

4\. If the status value is greater than the threshold, it sends the command "1 nabort" to the \`TargetCOMPort\`.

 

Make sure to adjust both \`ArduinoCOMPort\` and \`TargetCOMPort\` to the appropriate COM port numbers for your setup. Save the script with a \`.bat\` extension and run it. It will continuously monitor the voltage value from the Arduino and send the command to the specified \`TargetCOMPort\` whenever the threshold is exceeded.

 
