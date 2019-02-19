# Dynamic Cobb-Douglas Functions

Online version can be found here: cobb-douglas.henryzxu.com
 
## Short User Guide 
-The graphs are all generated using Dash by Plotly
- Alongside the main production function, there are two sets of points being plotted at all times, one for balanced growth equilibrium, and one for the path of a sample economy. You can toggle which one you'd like to see by clicking the associated section of the legend on the right. 
- The current time step is controlled by the slider immediately under the graph. To increase the maximum number of time steps, change the "Number of Time Periods" slider in the other section. 
- The **Basics** section controls alpha and the exogenous variables at time 0
- The **Experimental** section controls growth of the exogenous variables (so effectively growth of the growth). They're currently bounded below by 0 due to divide by zero issues with negative growth (if anyone has any ideas on how to fix this, please let me know!). 
-The **Other** section controls the total number of time periods and dynamic parameter changes.
- Format for dynamic parameter changes are as follows (multiple changes should be separated by commas):

  `<time period for your change to take effect> <parameter you which to change> <new value>`
  `Example: 10 n 0.06, 20 g 0.1`
 
-Troubleshooting
  1. If your dynamic changes don't show up, check if their effective time periods are before the current time period below the graph
  2. If other changes don't show up, it may be because it just affected the axes, or the web app crashed (see 7.)
Some issues with graphs ending early can be fixed by increasing the maximum number of time periods
  3. You can select a portion of the graph to zoom in on by just clicking and dragging on the graph
  4. Double clicking on the graph will reset it to normal
  5. As you increase the maximum number of time periods, changes will take longer and longer to take effect--please be patient! 
  6. Occasionally (or if you're playing with the experimental or dynamic parameter change sections, this will happen quite frequently) the web app may crash. There probably won't be a visual indication (I may fix this in the future), but the sliders most likely won't update anymore if you drag them. To fix this, just restart your webpage and it should reset to normal. **If you have any dynamic change inputs that you'd like to save, I'd highly recommend copy and pasting them somewhere else before refreshing.** 

