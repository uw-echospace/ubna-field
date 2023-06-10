# Welcome to the UBNA Bat Project!

## Introduction to the Audiomoth

This guide will hopefully help you with audiomoth deployment without feeling like there is something you’re forgetting.

The Audiomoth is an acoustic recorder meant for monitoring birds, bats, and other animals. They come equipped with a microphone capable of recording at ultrasonic frequencies. This makes them useful for monitoring bats via their echolocation calls.

## Useful Links

Below are a couple very useful guides that you can use to understand how to operate the Audiomoth:
1) https://github.com/rhine3/audiomoth-guide/blob/master/guide.md <- This a very articulate guide about field deployment of Audiomoths.
2) https://www.openacousticdevices.info/getting-started <- These people made the Audiomoth.

Open Acoustic Devices, the creators of the Audiomoth, also host a support forum where users can ask questions and find answers to asked questions. 
	The link is here: https://www.openacousticdevices.info/support

## What do we need for deployment?

1) Bring a portable laptop that can connect to the Audiomoth via USB, in case the Audiomoth needs reconfiguration or firmware updates.

2) Download the Audiomoth desktop apps on this laptop. The Audiomoth unit requires these apps to maintain its software, recording schedule/settings, and time.
	
	- Download Instructions can be found here: https://www.openacousticdevices.info/applications

	Note: The desktop apps will be are meant to reconfigure or update the Audiomoth while the mobile app plays the Audiomoth chime to reset date/time.

3) The Audiomoth's port is USB-microB. Bring a cable that can connect via USB from your laptop to the Audiomoth. The USB cable must also have data lines or else it cannot configure the Audiomoth. USB cables with data lines have four lines visible from either end: 2 standard charging lines and 2 data lines.

3) The Audiomoth saves its recordings onto microSD cards. You will need an empty microSD card for the Audiomoth to record into. The microSD cards we use are 128GB. This is large but sufficient for storing up to 96 hours worth of recordings at the sampling rate (192kHz) we are using to study our bats. 

4) A microSD to SD card adapter will also be useful to access those files in a computer that has an SD card slot. External SD card readers can also be used.

5) Rechargeable batteries. The Audiomoth units we use take up to 6 AA batteries. We currently use rechargeable AA batteries and are considering using other sources for power/energy.

6) Make sure your rechargeable batteries are fully charged by a rechargeable battery charger.

7) Bring a multimeter with a voltmeter to be able to check the Audiomoth's battery voltage.

8) Ziploc bags or Audiomoth cases to shield the Audiomoth from excessive rain while recording.

	If you use a ziploc bag, 

	- Find a way to black out the light emitted from the Audiomoth from inside the bag.

	- No need to make a hole for the Audiomoth unit’s microphone from inside the ziploc bag.

	- Although we want to ideally be able to reuse the ziploc bag for multiple deployments, do not hesitate to replace the ziploc bag if you notice any tears. It is preferable to keep the Audiomoth's exposure to environmental damage as little as possible.

	- Fold the bag around the Audiomoth and away from the microphone.

9) A long rubber cord or thread will be useful for keeping the Audiomoth wrapped and attaching it to its recording location.

10) You will also need your phone’s camera in order to take a picture of the deployment site. This is useful to remember when and where you deployed. Both of these are stored as the image’s metadata in your phone.

## How to properly extract Audiomoth from deployment site:

1) Remove Audiomoth from the deployment site and move to a secure location where you can open up materials with relative ease.

2) Take Audiomoth out of the case/ziploc bag and check the LEDs to check its status. There are many Audiomoth LED statuses but a few are the most common ones after a deployment session.
	
	a) No Green Light; Flashing Red Light w/ flash rate dependent on sampling rate: The Audiomoth is still recording. This means that neither the battery has died nor the SD card is full yet.
	
	![Recording](/DeploymentGuide/CommonLEDs/on_recording.png)
	
	a) No Red Light; Flashing Green Light: The Audiomoth is still on but in sleep mode because it has not been scheduled to record. This still means that neither the battery has died nor the SD card is full yet.
	
	![Recording](/DeploymentGuide/CommonLEDs/on_sleep.png)

	b) Both Lights Flash for 10ms; Pause; Repeat: This means that the Audiomoth has run into a recording error during its deployment. This might be because of the low battery or a full microSD card.
	
	![Error](/DeploymentGuide/CommonLEDs/error.png)
		
	Use this link for more information on the Audiomoth LED statuses:
https://www.openacousticdevices.info/led-guide

3) Switch the Audiomoth to USB/OFF mode.

4) Remove the microSD card and put it in a secure and memorable location. They are very easy to lose so make sure to store in a secure space.

5) Use the multimeter to check the Audiomoth's voltage as 'VOLTAGE_END'

6) Remove the batteries from the Audiomoth and place them somewhere secure and away from fully charged batteries to not mix them up.

## How to deploy your Audiomoth at deployment site:

1) Put the fully charged batteries into your Audiomoth unit and record Audiomoth battery voltage as 'VOLTAGE_START'.

2) Insert an empty microSD card inside the Audiomoth and write down the SD card's label in the Field Journal under 'SD Unit #'.

3) When you put in new batteries, the Audiomoth defaults its clock to 1/1/1970. We will use the acoustic chime to reset this clock after we turn the Audiomoth ON.

4) If the Audiomoth requires configuration, you can find pre-saved configs [here](/ConfigurationDetails) and use them to reconfigure the Audiomoth using the Configuration App. If the configuration was already loaded in for the previous deployment, you don’t have to load it in again. Time is the only setting that the Audiomoth resets after having batteries taken out, the configuration will remain with the Audiomoth.

5) Switch the Audiomoth to CUSTOM mode to turn it on. The Audiomoth will wait for a chime if it was not reconfigured using a laptop. Play the acoustic chime for the Audiomoth until it turns from solid green LED to blinking green/red LED. This means that it is recording without any errors.

	![Recording](/DeploymentGuide/CommonLEDs/on.png)

6) Pack up all your materials. You are now ready to deploy.
		
7) Put the Audiomoth back in its case/ziploc bag, and go back to your deployment site. Make sure you do not apply too much pressure onto the microSD card area when wrapping the cord around the Audiomoth. Sufficient pressure will make the card pop back out.

8) Use the rubber cord to reattach it to its branch and finally take a picture of the Audiomoth with your phone camera to remember when and where you deployed.

## Preparing for the next deployment:

1) Move all recordings from the microSD cards that were inside the Audiomoth unit into a sufficiently large external drive. You can store a copy on your computer as well if you plan to analyze the data but move the originals into the external drive.

	Note: Copying and moving the files between drives may take between 1-2hrs.

2) After all the recordings have been moved from the microSD card and are securely stored in an external drive, format your microSD card. This clears all memory and frees up all of its space to be used solely to store the next session’s recordings.

3) Charge your depleted rechargeable batteries. You may use your multimeter with a voltmeter to check your battery’s voltage before and after you charge them to ensure that they are fully charged. 

