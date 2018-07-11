# Tracking back-ends

Not all experiments need the same algorithms in order to successfully track features. For instance, 
dark-field images can have a very good signal-to-noise ratio and simple thresholding can achieve very
high frame-rates. Crowded samples may need better algorithms to distinguish features. And many more 
scenarios are possible. 

Implementing different back-ends should be easy to non-experienced UI programmers. That is the reason
behind monkey-patching libraries in this module. We will define some common variables that will be
interpreted by the UI in order to generate the different options. This is a plug-in sort of approach 
that opens to door to specific developments. 

## Trackpy
The *best* tracking library written in Python. It focuses into tracking gaussian-like objects in
2D and 3D. If you plan to use this back-end you need to install it yourself. You can find the 
[instructions here](http://soft-matter.github.io/trackpy/v0.4.1/installation.html). Trackpy makes 
extensive use of Pandas Dataframes, which are a different topic to cover. If you are not familiar 
with them, I suggest you to look them up. 

Trackpy offers different checks for our data, including if it is a color camera, the type of data 
generated, etc. This is handy for end-users, but has to be reviewed for live-streaming.

## Track 2D
This is a very simplified algorithm based on thresholding and grouping of pixels. It looks at groups of pixels above a 
given threshold. If some criteria is met, it is qualified as a particle. This algorithm is very fast, can reach 1000fps 
on data of around 550x550px. 