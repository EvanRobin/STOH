import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

'''
U ovom kodu racuna se standardna devijacija energetskih vrijednosti iz "E.txt".
'''

#kod za racunanje srednje vrijednosti i standardne devijacije
Nkmax = 200
fE = np.loadtxt('E.txt', comments='#')
fstdev = open('st_dev_E.dat', 'w') #file za graf
N = len(fE)

for Nk in range(1, Nkmax+1):
    Nb = N//Nk #koriste se samo cijeli blokovi
    if Nb <= 2: #ne analiziraju se blokovi s 2 ili manje podataka (losa statistika)
        continue
    Sfb, Sf2b = 0.0, 0.0 #suma srednjih vrijednosti po bloku
    for b in range(Nb):
        block = fE[b*Nk : (b+1)*Nk, 1]  #uzima vrijednosti samo iz 2. stupca "E.txt"
        Sfk = np.sum(block)
        Sfb += Sfk/Nk
        Sf2b += (Sfk*Sfk)/(Nk*Nk)
    #extra = fE[Nb * Nk :, 1] #ostatak ako se podaci ne raspodjele cjelobrojno
    #n = len(extra)
    #if n > 0:
        #nepun = True
        #Sfk = np.sum(extra)
        #Sfb += Sfk/n
        #Sf2b += Sfk**2/n**2
        #Nb += 1  #zbog parcijalnih blokova
    var = ((Sf2b/Nb)-(Sfb/Nb)**2)/(Nb-1) #varijanca
    fstdev.write(f"{Nk:<3d} {Sfb/Nb:>12.7f} {np.sqrt(var):>10.7f}\n")
        
fstdev.close()

fEdev0 = np.loadtxt('E_dev.dat', comments='#')
fEdev = np.loadtxt('st_dev_E.dat')

b, mE, devE, dev0 = [], [], [], []
for i in range(Nkmax):
    b.append(fEdev[i, 0])
    mE.append(fEdev[i, 1])
    devE.append(1000*fEdev[i, 2])
    dev0.append(1000*fEdev0[i, 1])

mdev = f"{np.mean(devE)/1000:<5.3f}"

fig = plt.figure(figsize=(8,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.plot(b, dev0, color='blue', lw=1.7, label='original')
ax.plot(b, devE, color='red', lw=1.3, linestyle='-.', label='dobivena blokiranjem')
ax.set_xlim(0, 200)
ax.set_ylim(15, 70)
ax.set_xlabel('b / 2000')
ax.set_ylabel('$10^{3} \u03C3_{E}$ / mK')
ax.xaxis.set_major_locator(tick.MultipleLocator(20))
ax.yaxis.set_major_locator(tick.MultipleLocator(5))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Standardna devijacija $\u03C3_{E}$ energije samovezanja $E$ klastera\n$^{4}$He$_{20}$ za vremenski korak $\u0394\u03C4=10^{-7}$ mK$^{-1}$')
ax.legend(loc='upper right')
ax.text(10, 65, s='$\u03C3_{}$={} mK'.format('E', mdev))
plt.show()

'''fig = plt.figure(figsize=(10,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.errorbar(b, mE, yerr=devE, fmt='o-', capsize=2, label='energija', ecolor='purple', elinewidth=0.3,
            mfc='red', mec='purple', ms=5, mew=1)
ax.set_xlim(0, 200)
ax.set_ylim(-85.06, -84.88)
ax.set_xlabel('b / 2000')
ax.set_ylabel('<E> / mK')
ax.xaxis.set_major_locator(tick.MultipleLocator(20))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.02))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Srednja vrijednost energije samovezanja $E$ klastera $^{4}$He$_{20}$ za\nvremenski korak $\u0394\u03C4=10^{-7}$ mK$^{-1}$ dobivena dodatnim blokiranjem')
ax.legend(loc='upper right')
plt.show()'''