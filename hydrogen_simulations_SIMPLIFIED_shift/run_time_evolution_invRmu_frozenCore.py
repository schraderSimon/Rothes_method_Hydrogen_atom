from time_evolution_and_optimization_frozen import *

avals20_opt_mu100=[0.37975054516979373, 0.6727106754496565, 1.6170983925847966, 2.1872731735075677, 0.8973641814587451, 0.28361222429044125, 2.9749499071117103, 5.60338912643523, 0.5055386682291061, 10.837178847969009, 15.236731452010996, 21.58780176075342, 4.070161687631614, 7.765343237447249, 30.81229158951304, 44.17912046702323, 62.86671909155382, 1.2017817216272368, 0.20778210978566386, 85.22431895159728]
cvals20_opt_mu100=np.array([-0.15109892140859937, -0.27661419521848174, -0.18969931007124785, -0.14904092900510335, -0.2671980148315303, -0.05298055481537434, -0.11428168641197267, -0.06422868801471893, -0.23939555871049922, -0.03452587899271009, -0.024830081172808605, -0.017484899664552245, -0.08620241602383594, -0.04735030547787389, -0.011842902169146186, -0.007362528835059834, -0.0036642396706092484, -0.2323388708049059, -0.005526709229205784, -0.0009177620378704177])/np.sqrt(4*pi)*np.array([(5.995733193439505+0j), (2.5430062540313325+0j), (0.6823155039033278+0j), (0.4337458854863377+0j), (1.650580887275071+0j), (9.289717105617125+0j), (0.2734452739473841+0j), (0.10578247724497705+0j), (3.9035373373125495+0j), (0.03932923933024014+0j), (0.023591317092997017+0j), (0.013988697402321861+0j), (0.17087259492921766+0j), (0.06484088331638208+0j), (0.008203589283689632+0j), (0.004778199840547195+0j), (0.0028148724079561814+0j), (1.065004679990896+0j), (14.814182147440023+0j), (0.0017833829026512409+0j)])
cvals25_opt_mu100=[0.02780073388485027, 0.021455573255479976, 0.1981382882211875, 0.14176331648482687, 0.22027713190778186, 0.1628440255345336, 0.2281368878986081, 0.03593284782994033, 0.027871597457533426, 0.09308946667465534, 0.21133043228579718, 0.0741479700014338, 0.006166918028363, 0.01635480201062478, 0.17017840429073772, 0.11569135021079546, 0.046026229604819946, 0.05860523458181888, 0.002492513492044903, 0.012265696410295845, 0.0019066008768753306, 0.008929086495939487, 0.0038572482840049105, 0.09085917010094502, 0.0004629295004452416]*np.array([10.659781694951377, 0.027209830718553027, 1.2065348943803709, 0.5860145787920756, 1.7226258882338337, 5.009225278597745, 2.454801662835785, 0.06042571567789139, 0.040658683706854194, 0.280007539373264, 3.499373335865126, 0.19224932639695994, 0.0051902478676147225, 0.01810664510632858, 0.8424397774113559, 0.4059645753823523, 0.08932613974979091, 0.1313696650804917, 16.27555649926271, 0.011979558971113934, 0.0023138837992114835, 0.007889413201769157, 0.003432409536796411, 7.241616252836806, 0.0016596784648964975])/(sqrt(4*np.pi))
avals25_opt_mu100=[0.2587583648224493, 13.854027496228941, 1.105859655044476, 1.789730578043443, 0.872166280519578, 0.42810098736664876, 0.6887299979920632, 8.139144082427972, 10.599638699980089, 2.9282857568011305, 0.5437506047471511, 3.7625595940674823, 41.80881638029523, 18.176124085549866, 1.4050788460506318, 2.2859558910621125, 6.2720218264539565, 4.849867533706469, 0.1951503676612846, 23.938635131860458, 71.64164922272775, 31.624971067039272, 55.0799924264482, 0.3348391780641226, 89.40818923139646]


invR_mu=100.0
nExtra=25
cvals=np.concatenate((cvals25_opt_mu100,np.zeros(nExtra)))
avals=np.concatenate((avals25_opt_mu100,np.logspace(-1,1,nExtra)))
avals[40]*=2.5
avals[30]/=2
avals[35]=1.3
avals[34]/=2
avals[36]*=2

avals[39]/=2
avals[45]*=2
avals[48]/=2
avals[44]/=2

muvals=np.concatenate((np.zeros(len(cvals)-nExtra),np.linspace(0,0.1,nExtra)))
muvals[31]=0.5
print(avals)
#cvals=cvals20_opt_mu100
#avals=avals20_opt_mu100

params=np.zeros((len(cvals))*4)
params[::4]=np.array(avals)
params[2::4]=np.array(muvals)

import os
t0=0
try:
    E0=float(sys.argv[1])
    epsilon=float(sys.argv[2])
    t0=float(sys.argv[3])
except:
    E0=0.03
    epsilon=0.005
    t0=30
try:
    h=float(sys.argv[4])
except:
    h=0.05
error_t0=0
omega = 0.057
t_cycle = 2 * np.pi / omega
td = 3 * t_cycle
err_t0=0
hlm=False # True False False, ALT
def sine_field_func_noRegular(t):
    return np.sin(omega * t)* E0

def sine_field_func(t):
    t_cycle = 2 * np.pi / omega
    td = 3 * t_cycle
    dt = t
    pulse = (
        (np.sin(np.pi * dt / td) ** 2)
        * np.heaviside(dt, 1.0)
        * np.heaviside(td - dt, 1.0)
        * np.sin(omega * dt)
        * E0
    )
    return pulse
def fieldfunc(t):
    return sine_field_func(t)
filename="outputs/NEWNEW/data_E0%.3f_omega%.3f_invRmu%d_dt%.2f_epsilon%.2e_frozenCore.h5"%(E0,omega,invR_mu,h,epsilon)
if t0>=h-0.00001:
    try:
        with h5py.File(filename, "r+") as data_file:
            times=np.array(data_file["times"])
            t0_index=np.argmin(abs(times-t0))
            params=np.array(data_file["parameters_t=%.2f"%t0])
            cvals=np.array(data_file["coefficients_t=%.2f"%t0])
            err_t0=np.array(data_file["rothe_error"])[t0_index]
            try:
                data_file.create_dataset("dpm_backup", data=np.array(data_file["dpm"]))
                data_file.create_dataset("times_backup", data=times)
            except:
                pass
    except:
        t0=0; err_t0=0

tfinal = td
wave_function=erf_WF(params=params,basis_coefficients=cvals,fieldFunc=fieldfunc,potential_params=[invR_mu])
a=wave_function.overlap_normalized-np.diag(np.diag(wave_function.overlap_normalized))
print(np.unravel_index(a.argmax(), a.shape))
print(a[np.unravel_index(a.argmax(), a.shape)])
#sys.exit(1)
#print("Normalization:")
#print(np.conj(wave_function.coefficients).T@wave_function.overlap_normalized@wave_function.coefficients)
timeEvolver=TimeEvolution(wave_function,fieldFunc=sine_field_func,potential_params=[invR_mu],potential_type="erf",h=h,T=tfinal,epsilon=epsilon,t0=t0,error_t0=err_t0,filename=filename,hlm=hlm)
timeEvolver.time_evolve()
