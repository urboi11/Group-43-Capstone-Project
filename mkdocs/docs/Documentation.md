## Settings
*Thresholds- These affect the threshold of confidence for the AI. It is essentially a confidence score. Setting the SSN to .8 for example would ask the program to filter the document for SSN's if the confidence score given by the ai is above 80%.
*Output Location- This is where your output will be stored. Hit browse to go to the file location with browse you can set any folder as the output folder
*Logging Location-This is where logs saved in a txt format for ease of use.
*Batch size: Batch size controls how many token sequences (or chunks) the model processes at once during inference or training, affecting speed and memory usage.
*Merge gap: Merge gap defines the maximum number of characters allowed between adjacent detected fragments for them to be combined into a single merged PII span.