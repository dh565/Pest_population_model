**RS-PestDyn**

This is a python code of an insect pest population dynamics model, which currently simulates one life stage of a generic pest for a single day. The model uses a numerical solution for the differential equation of an age distribution function through a  Runge-Kutta method. The main driver of the model is temperature, which is satellite-derived (the 1km, daily land surface temperature MODIS product) used as daily input to the model. To view the basics of this model (with Euler solution) see [Blum et al. 2018](https://www.sciencedirect.com/science/article/pii/S0304380017305021).

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
5) add plant growth
6) add migration between pixels
