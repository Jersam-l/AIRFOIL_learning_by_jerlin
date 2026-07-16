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
print("EXTERNAL DOMAIN TYPE\n	(1)=External Aerodynamics[DEFAULT]\n	(2)=Wind Tunnel\n	(3)=custom Domain")
domain_type=int(input("select an option :"))

if domain_type==1:
	print("External Aerodynamics [default] domain selected")
	upstream=5
	downstream=15
	top_distance=10
	bottom_distance=10
elif domain_type==2:
	print("Wind Tunnel domain selected")
	blockage= float(input("Enter the required blockage ratio (%) [recomended=3 or 5] :"))/100
	upstream=float(input("Enter the upstream distance [x chord length] (recomended:5):"))
	downstream=float(input("enter the down stream distance [x chord length] (recomended:6 or 10):"))
elif domain_type==3:
	print("Custom domain selected")
	upstream=float(input("enter upstream distance[x chord] :"))
	downstream=float(input("Enter the down stream distance [x chord]:"))
	top_distance=float(input("Enter the Top distance[x chord]:"))
	bottom_distance=float(input("Enter the bottom distance [x chord]:"))
else:
	print("Invalid option selected ")
	exit()
print("DOMAIN SHAPE\n	(1)=Rectangle[Default]\n	(2)=C-Domain[semi-circular inlet]\n")
#print("	(3)=O-Domain[Circular farfield]\n       (4)=[Custom Domain]")
domain_shape=int(input("Select an option:"))

c=float(chord) #chord length
n=int(points) #number of points
# x coordinate
x=np.linspace(0,c,n)
m=int(airfoil[0])/100   #chamber
p=int(airfoil[1])/10    #position of the chamber
t=int(airfoil[2:])/100  #thickness
if p==0:
	print("Error: Second digit of the naca 4 digit airfoil cant be zero!")
	exit()

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
#for outer  domain
left =-upstream*c
right=downstream*c
max_thickness=np.max(yu-yl)
if domain_type==2:
	tunnel_height=max_thickness/blockage
	top=tunnel_height/2
	bottom=-tunnel_height/2
else:
	top=top_distance*c
	bottom=-bottom_distance*c
top_x=np.linspace(left,right,200)
top_y=np.full(200,top)
right_x=np.full(200,right)
right_y=np.linspace(top,bottom,200)
bottom_x=np.linspace(right,left,200)
bottom_y=np.full(200,bottom)

if domain_shape==1:
	outer_boundary_x=np.array([left, right, right, left, left])
	outer_boundary_y=np.array([bottom, bottom, top, top, bottom])
elif domain_shape==2:
	degrees=np.linspace(270,90,500)
	theta_arc=np.deg2rad(degrees)
	arc_x=left+top*np.cos(theta_arc)
	arc_y=top*np.sin(theta_arc)
	outer_boundary_x=np.concatenate((top_x,right_x[1:],bottom_x[1:],arc_x[1:]))
	outer_boundary_y=np.concatenate((top_y,right_y[1:],bottom_y[1:],arc_y[1:]))
#elif domain_shape==3:
        #0-domain
#elif domain_shape==4:
        #custom domain
else:
        print("error:invalid input")
        exit()
#foil
airfoil_boundary_x=np.concatenate((xu[::-1],xl[1:]))
airfoil_boundary_y=np.concatenate((yu[::-1],yl[1:]))


print(left)
print(top)
print(bottom)

print(arc_x[0], arc_y[0])
print(arc_x[-1], arc_y[-1])

plt.figure(figsize=(10,4))
#plt.plot(outer_boundary_x,outer_boundary_y,label="computationalddomain")
plt.plot(outer_boundary_x, outer_boundary_y, "-o", markersize=2)
plt.plot(airfoil_boundary_x,airfoil_boundary_y,label="airfoil surface") 
plt.plot(x,yc,"--",label="chamber line")
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()  
exit()

filename=f"NACA{int(m*100)}{int(p*10)}{int(t*100)}.dat"
with open(filename,"w") as file:
	for i in range(len(boundary_x)):
		file.write(f"{boundary_x[i]:.8f} {boundary_y[i]:.8f}\n")
