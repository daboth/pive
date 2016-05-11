### 0.3.4
**Major changes**

 * Fixed path issues for windows operating systems while loading the templates.
 * The path where the dataset is generated can now be explicitly passed (optional).
 * Optionally returns the generated javascript code as a String only.
 * Datetime datapoints are now validated automatically while determining the visualization types.
   Iso formatted dates and Unix-Timestamps need to be provided as Strings. 

**Minor changes**

 * Refactored some code in favor of readability.

### 0.3.3
**Major changes**

 * Modified the chart generation. No more CSS documents will be generated. CSS styles
   are included within the javascript template directly.
 * Users can now pass a destination div container (div_hook) to tell pive where to put
   the visualization in a web document.
 * New environment function allows users to only obtain the plain javascript code and its data.

**Minor changes**

 * Refactoring
 * Cleanup
 * Added sample data
 * Added sample charts

### 0.2.3
**Major changes**
 * Fixed an issue while creating the chords in chordchart.

**Minor changes**
 * Added a 'pive powered' badge.
 * Added initial sphinx documentation.

### 0.2.2
**Major changes**
 * Fixed an issue where visualization types were not correctly read.

**Minor changes**
 * Refactoring
 * Cleanup

### 0.2.1
**Major changes**

 * First working version of pive: No changes documented.
