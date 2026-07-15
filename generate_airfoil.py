import numpy as np
import matplotlib.pyplot as plt

airfoil=(input("Enter the 4 digits of the NACA series whose coordinates were needed :"))
if len(airfoil)!=4:
	print("Bruh this is for 4 digit airfoil enter 4 digits only  this is an error .")
	exit()
elif len(airfoil)<4:
	print("Bruh this is for 4 digit airfoil enter 4 digits only  this is an error .")
	exit()

chord=(input("Enter the required chord length :"))
points=(input("Enter the  number of point's needed for the coordinates (whole number) :"))

c=float(chord) #chord length
n=int(points) #number of points
# x coordinate
x=np.linspace(0,c,n)
m=int(airfoil[0])/100   #chamber
p=int(airfoil[1])/10    #position of the chamber
t=int((airfoil[2:]))/10  #thickness

xu=np.zeros(n)
yu=np.zeros(n)
xl=np.zeros(n)
yl=np.zeros(n)
yc=np.zeros(n)
yt=np.zeros(n)
theta=np.zeros(n)

for i,xi in enumerate(x):
	yt[i]=5*t*(0.2969*np.sqrt(xi)-0.1260*xi-0.3516*xi**2+0.2843*xi**3-0.1036*xi**4)

	if xi <= p*c:
		yc[i]=(m/(p**2))*(2*p*xi-xi**2)
		dyc_dx=(m/p**2)*(2*p-2*xi)
	else:
		yc[i]=(m/((1-p)**2))*((1-2*p)+2*p*xi-xi**2)
		dyc_dx=(m/(1-p)**2)*(2*p-2*xi)
	theta[i]=np.arctan(dyc_dx)

xu=x-yt*np.sin(theta)
yu=yc+yt*np.cos(theta)
xl=x+yt*np.sin(theta)
yl=yc-yt*np.cos(theta)

boundary_x=np.concatenate((xu[::-1],xl[1:]))
boundary_y=np.concatenate((yu[::-1],yl[1:]))

filename=f"NACA{int(m*100)}{int(p*10)}{int(t*100):02d}.dat"
with open(filename,"w") as file:
	for i in range(len(boundary_x)):
		file.write(f"{boundary_x[i]:.8f} {boundary_y[i]:.8f}\n")
