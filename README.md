**RS-PestDyn**

The **R**emote **S**ensing insect **Pest** **Dyn**amic model is an insect pest population dynamics model driven by temperature, which is derived from satellites at a daily basis. The satellite data used is the 1km land surface temperature (LST) product of MODIS, which is directly downloaded from Google Earth Engine. LST is then used in **RS-PestDyn** as a daily input to the model while a series of ordinary differential equations (ODEs) are solved simulataneously through the Runge-Kutta method for daily simulations of insect pest populations. Currently, **RS-PestDyn** simulates the population of a generic pest for a single life stage and for one day only. It still lacks several processes, which are matained constant at this stage. For more information on the basics of this model (using Euler solution) see [Blum et al. 2018](https://www.sciencedirect.com/science/article/pii/S0304380017305021).

*Main program to run:*
* 'run_RK4_2D.py'

*Procedures called:*
* 'Download_Temp_GEE.py' - download TIF files of LST from MODIS as a batch from GEE
* 'RK4_2D_procedure.py'  - solves the ODE using Runge-Kutta
* 'display_plots.py'     - displays results (as a 2D matrix of % population)

*Still needs:*
1) extend to entire period (currently for 1 day)
2) extend to other life stages (currently only 1)
3) improve solution for error expansion through time.
4) add LC/LU classification
5) add plant growth dynamics
6) add migration between grid cells
