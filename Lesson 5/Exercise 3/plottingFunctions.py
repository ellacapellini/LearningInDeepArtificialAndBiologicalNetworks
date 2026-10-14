import numpy as np
import matplotlib.pyplot as plt
import time
import networkx as nx
import pandas as pd
import seaborn as sns
from netgraph import Graph
from matplotlib.colors import LinearSegmentedColormap
import matplotlib


def plotNetwork(self):
		
    ### General stuff

    # Generate weight matrix (weight between neurons are summed, eg. weight between PN 1 and 4 == 4 and 1)
    weight_matrix = np.zeros((self.n_PN,self.n_PN))
    for i in range(self.n_PN):
        for j in range(self.n_PN):
            weight_matrix[i,j] = self.weightPN_PN[-1,i,j] + self.weightPN_PN[-1,j,i]

    ### Generate Graph
    G = nx.from_numpy_array(weight_matrix)

    # Set node shape
    node_shape = {i: 'o' for i in G.nodes()}

    node_edge_width = {i: 0.5 for i in G.nodes()}
    node_edge_color = {i: 'black' for i in G.nodes()}
    ### set colors
    # If a neuron belongs to different ensembles, it gets colored according to the ensemble it showes the strongest activity in.
    # Only checks pair wise and not if eg it is in all three lists.

    
    color = {}
    for i in G.nodes():
        color[i] = '#ede8e4'

    for i in self.ensembleNeurons[0]:
        color[i] = self.color[0]

    # Check if neurons belong to multiple ensembles.
    overlay = 0
    for i in self.ensembleNeurons[1]:
        if i in self.ensembleNeurons[0]:
            color[i] = '#6C7D8A'
            overlay = 1
        else:
            color[i] = self.color[1]

    # DONE COLOR
    self.colors = color	

    weight = nx.get_edge_attributes(G,'weight')
    edges = G.edges()
    width = {key: weight[key] / 4 for key in weight} # Used to draw the thickness of the connections (needs to be scaled down a bit to not be too thick...)


    #Generate edge colors		
    norm = matplotlib.colors.Normalize(vmin=0, vmax=np.max(weight_matrix))
    # Choose colormap
    #cmap = pl.cm.autumn_r
    cmap = matplotlib.cm.autumn_r
    edgeCol = {key: cmap(norm(weight[key])) for key in weight.keys()}


    # Code to add an increasing alpha value in addition to the color map
    '''
    my_cmap = cmap(np.arange(cmap.N))
    my_cmap[:,-1] = np.linspace(0, 1, cmap.N) # Set alpha
    # Create new colormap
    my_cmap = ListedColormap(my_cmap)
    # Create color 'edgeCol'
    edgeCol = {key: my_cmap(norm(weight[key])) for key in weight.keys()}
    '''
    


    node_proxy_artists = []
    # Create proxy artists for legend handles.
    if overlay == 1:
        legend_color = ['#1f77b4','#7f7f7f', '#6C7D8A']
        legend_label = ['teacher', 'control', 'overlay']
        for node in range(self.n_VIP+2):
            proxy = plt.Line2D([], [], linestyle='None', color=legend_color[node],label=legend_label[node], marker=node_shape[node], markersize=8)
            node_proxy_artists.append(proxy)

    else:
        legend_color = self.color
        legend_label = ['teacher', 'control']
        for node in range(self.n_VIP+1):
            proxy = plt.Line2D([], [], linestyle='None', color=legend_color[node],label=legend_label[node], marker=node_shape[node], markersize=8)
            node_proxy_artists.append(proxy)


    





    # Calculate the position of nodes
    pos = nx.spring_layout(G, scale = 0.5)


    # Plot graph
    fig, ax = plt.subplots(figsize=(20,10))
    g = Graph(list(edges), 
        node_layout = pos,
        node_layout_kwargs=dict(edge_length=weight),
        ax=ax,
        edge_width = width,
        edge_color = edgeCol,
        node_size=2,
        node_labels=True,
        node_color=color,
        node_edge_width = node_edge_width,
        node_edge_color = node_edge_color
        )

    
    ax.set_aspect('equal')

    # Add legend
    node_legend = ax.legend(handles=node_proxy_artists, fontsize = 12, framealpha=0)
    ax.add_artist(node_legend)
    
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    clb = plt.colorbar(sm, ax = ax, shrink = 0.5)
    clb.ax.set_title('Weights')





    plt.show()

def plotActivityPub(self):
    '''
    Plots the input, evolution of weights and evolution of output/activity in one plot.
    For "save == True" a subfolder is created (see documentation in _makeDir()) and the generated plots are saved there. Further,
    a .txt file is saved containing all parameters used for initializaiton of the neuron as well as some additional information. 
    '''
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    Llim = (-0.1,0.9)
    Rlim = (self.time_s-1,self.time_s)
    d = .015  # how big to make the diagonal lines in axes coordinates
    mypad = 0.4
    ####################################################
    
    time = np.linspace(0, self.time_s, num = self.time_ms)

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, gridspec_kw={'height_ratios': [6, 2, 2, 2, 1]}, sharex=True,figsize=(10,6))


    # Divide plot into two parts (broken x-axis)
    divider = make_axes_locatable(ax1)
    ax1R = divider.new_horizontal(size="100%", pad=mypad)
    fig.add_axes(ax1R)

    # plot the same data on both axes
    # Plot PN
    for j in range(self.n_PN):
        ax1.plot(time,self.Activity_PN[j,:],linewidth=1)
        ax1R.plot(time,self.Activity_PN[j,:],linewidth=1)

    # Limit in seconds
    ax1.set_xlim(Llim)
    ax1R.set_xlim(Rlim)

    ax1R.set_xticklabels([])
    ax1R.set_yticklabels([])

    ax1.set_title("PN",y=1.0, pad=-9)
    ax1R.set_title("PN",y=1.0, pad=-9)

    # hide the spines between ax and ax2
    #ax1.spines['right'].set_visible(False)
    #ax1R.spines['left'].set_visible(False)
    #ax1.tick_params(labelright='off')
    
    



    '''
    # Plot PN
    for j in range(self.n_PN):
        ax1.plot(time,self.Activity_PN[j,:])
    ax1.set_title("PN",y=1.0, pad=-14)
    # Decrease width of blox to leave space for legend.
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    '''

    # Divide plot into two parts (broken x-axis)
    divider = make_axes_locatable(ax2)
    ax2R = divider.new_horizontal(size="100%", pad=mypad)
    fig.add_axes(ax2R)

    # Plot SST
    for j in range(self.n_SST):
        ax2.plot(time,self.Activity_SST[j,:],linewidth=1)
        ax2R.plot(time,self.Activity_SST[j,:],linewidth=1)
    
    ax2.set_title("SST",y=1.0, pad=-9)
    ax2R.set_title("SST",y=1.0, pad=-9)
    # Decrease width of blox to leave space for legend.
    # = ax2.get_position()
    #ax2.set_position([box.x0, box.y0, box.width * 0.9, box.height])


    # Limit in seconds
    ax2.set_xlim(Llim)
    ax2R.set_xlim(Rlim)

    ax2R.set_xticklabels([])
    ax2R.set_yticklabels([])



    # Plot PV

    # Divide plot into two parts (broken x-axis)
    divider = make_axes_locatable(ax3)
    ax3R = divider.new_horizontal(size="100%", pad=mypad)
    fig.add_axes(ax3R)


    for j in range(self.n_PV):
        ax3.plot(time,self.Activity_PV[j,:],linewidth=1)
        ax3R.plot(time,self.Activity_PV[j,:],linewidth=1)

    ax3.set_title("PV",y=1.0, pad=-9)
    ax3R.set_title("PV",y=1.0, pad=-9)
    '''	
    ax3.set_title("PV",y=1.0, pad=-12)
    box = ax3.get_position()
    ax3.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    '''


    # Limit in seconds
    ax3.set_xlim(Llim)
    ax3R.set_xlim(Rlim)


    ax3R.set_xticklabels([])
    ax3R.set_yticklabels([])


    # Plot VIP

    # Divide plot into two parts (broken x-axis)
    divider = make_axes_locatable(ax4)
    ax4R = divider.new_horizontal(size="100%", pad=mypad)
    fig.add_axes(ax4R)



    for j in range(self.n_VIP):
        ax4.plot(time,self.Activity_VIP[j,:], label = "VIP " + str(j+1),linewidth=1)
        ax4R.plot(time,self.Activity_VIP[j,:], label = "VIP " + str(j+1),linewidth=1)
    

    #ax4.set_title("VIP",y=1.0, pad=-12)

    # Decrease width of blox to leave space for legend.
    #box = ax4.get_position()
    #ax4.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    #leg = ax4.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # Put a legend to the right of the current axis
    

    # change the line width for the legend
    #for line in leg.get_lines():
    #	line.set_linewidth(1.5)
    
    # Limit in seconds
    ax4.set_xlim(Llim)
    ax4R.set_xlim(Rlim)
    ax4R.set_xticklabels([])
    ax4R.set_yticklabels([])

    ax4.set_title("VIP",y=1.0, pad=-9)
    ax4R.set_title("VIP",y=1.0, pad=-9)

    myinput = np.sum(self.input, axis=0) / 2

    '''
    for i in range(self.n_inputs):
        ax5.vlines(time, np.zeros(self.time_ms), myinput,linewidth=0.4, color='gray', label = "input")
    '''

    #rainbow = ax5._get_lines.prop_cycler

    
    teacher1 = np.zeros(self.time_ms)
    randinpt = np.zeros(self.time_ms)
    for i in range(self.time_ms):
        if myinput[i] == 1 and self.teacher[0,i] == 1:
            teacher1[i] = 1
        elif myinput[i] == 1 and self.teacher[0,i] != 1:
            randinpt[i] = 1





    # Plot VIP

    # Divide plot into two parts (broken x-axis)
    divider = make_axes_locatable(ax5)
    ax5R = divider.new_horizontal(size="100%", pad=mypad)
    fig.add_axes(ax5R)

    ax5.vlines(time, np.zeros(self.time_ms), teacher1 ,linewidth=0.4, color = '#4C72B0', label = "input + teacher 1")
    ax5.vlines(time, np.zeros(self.time_ms), randinpt ,linewidth=0.4, color ='gray', label = "input w/o teacher")

    ax5R.vlines(time, np.zeros(self.time_ms), teacher1 ,linewidth=0.4, color = '#4C72B0', label = "input + teacher 1")
    ax5R.vlines(time, np.zeros(self.time_ms), randinpt ,linewidth=0.4, color ='gray', label = "input w/o teacher")


    # Limit in seconds
    ax5.set_xlim(Llim)
    ax5.set_ylim(0,2)
    ax5R.set_xlim(Rlim)
    ax5R.set_ylim(0,2)
    ax5R.set_yticklabels([])

    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-d, -1), (d, 1)], markersize=12,
      linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax5.plot(1, 0, transform=ax5.transAxes, **kwargs)
    ax5R.plot(0, 0, transform=ax5R.transAxes, **kwargs)


    ax5.set_title("input",y=1.0, pad=-9)
    ax5R.set_title("input",y=1.0, pad=-9)
    '''
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax5.transAxes, color='k', clip_on=False)
    ax5.plot((1-d, 1+d), (-d, +d), **kwargs)
    #ax1.plot((1-d, 1+d), (1-d, 1+d), **kwargs)

    kwargs.update(transform=ax5R.transAxes)  # switch to the bottom axes
    #ax1R.plot((-d, +d), (1-d, 1+d), **kwargs)
    ax5R.plot((-d, +d), (-d, +d), **kwargs)

    '''
    '''
    # Shrink current axis by 20%
    box = ax5.get_position()
    ax5.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # Put a legend to the right of the current axis
    leg = ax5.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    

    #leg = ax5.legend()
    ax5.set_title("Input",y=1, pad=-12)
    ax5.set_xlabel("time (s)",fontsize=14)
    ax5.set_ylim((0,2))
    


    # change the line width for the legend
    for line in leg.get_lines():
        line.set_linewidth(1.5)

    '''
    fig.text(0.07, 0.5, 'activity (rate)', va='center', rotation='vertical',fontsize=14)
    fig.text(0.49, 0.05, 'time (s)', va='center', rotation='horizontal',fontsize=14)
    #ax1.text(0.5, 1,1, 'untrained')
    #fig.text(0.685, 0.9, 'trained', va='center', rotation='horizontal',fontsize=14,verticalalignment='top',horizontalalignment='center')
    




    plt.show()

def plotConnectivity(self):

    colors = ["lightgray","gray"] 
    cmap = LinearSegmentedColormap.from_list('Custom', colors, len(colors))


    # PN to PN connection
    fig, ax = plt.subplots()
    sns.heatmap(self.conPN_PN, ax=ax, cmap=cmap,square=True,  linewidths=.5, cbar_kws={"shrink": .1, "aspect": 2})
    ax.set_title("PN to PN")
    colorbar = ax.collections[0].colorbar		
    colorbar.set_ticks([0.25,0.75])
    colorbar.set_ticklabels(['not connected', 'connection'])

    plt.show()

    '''
    # PN to PV and PN to SST connection
    fig, (ax1, ax2) = plt.subplots(nrows = 2)
    sns.heatmap(self.conPN_PV, ax=ax1, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    sns.heatmap(self.conPN_SST, ax=ax2, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    ax1.set_title("PN to PV ")
    ax2.set_title("PN to SST")

    plt.show()


    # PV to PN and SST to PN
    fig, (ax1, ax2) = plt.subplots(ncols = 2)
    sns.heatmap(self.conPV_PN, ax=ax1, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    sns.heatmap(self.conSST_PN, ax=ax2, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    ax1.set_title("PV to PN ")
    ax2.set_title("SST to PN")

    plt.show()
    

    # VIP to SST and SST to PV and PV to PV
    fig, (ax1) = plt.subplots(ncols = 1)
    sns.heatmap(self.conVIP_SST, ax=ax1, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    #sns.heatmap(self.conSST_PV, ax=ax2, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    #sns.heatmap(self.conPV_PV, ax=ax3, cmap=cmap, square=True,  linewidths=.5, cbar = False)
    ax1.set_title("VIP to SST ")



    plt.show()
    '''

def plotEnsembleWeights(self):

    from scipy.stats import sem
    # Number of repeatedly presented input w/o teacher signal
    import matplotlib as mpl
    mpl.rcParams['path.simplify'] = True
    mpl.rcParams['path.simplify_threshold'] = 1.0


    # Store Means and standard deviation of within ensemble weight evolution
    self.withinWeights_Mean = np.zeros((self.n_VIP+self.n_randInputs, self.time_ms))
    self.withinWeights_SD = np.zeros((self.n_VIP+self.n_randInputs, self.time_ms))

    # Store Means and standard deviation of between ensemble weight evolution
    self.betweenWeights_Mean = np.zeros(self.time_ms)
    self.betweenWeights_SD = np.zeros(self.time_ms)


    # Store the indexes of neurons that are not in an ensemble.
    tempConnMatrix_Between = np.full((self.n_PN,self.n_PN),False)
    # Set all connections between the neurons in an ensemble to True, without allowing recurrent connections.
    for VIP in range(self.n_VIP + self.n_randInputs):
        
        # Temp matrix used to store index of ensemble connections (used to index weight matrix.)
        tempConnMatrix = np.full((self.n_PN,self.n_PN),False)
        
        # Loop trough all possible connections in the ensemble
        for i in self.ensembleNeurons[VIP]:
            for j in self.ensembleNeurons[VIP]:
                # Check if the neurons are really connected:
                if self.conPN_PN[i,j] == 1:
                    tempConnMatrix[i,j] = True

        
        # Calculate the mean and SD for each ensemble.
        self.withinWeights_Mean[VIP,:] = np.average(self.weightPN_PN[:,tempConnMatrix],axis=1)

        #self.withinWeights_SD[VIP,:] = np.std(self.weightPN_PN[:,tempConnMatrix],axis=1)
        self.withinWeights_SD[VIP,:] = sem(self.weightPN_PN[:,tempConnMatrix],axis=1)

    

    

    # Get weight evolution between two ensembles (only works for two VIPs at the time...)
    tempConnMatrix = np.full((self.n_PN,self.n_PN),False)
    for i in self.ensembleNeurons[0]:
            for j in self.ensembleNeurons[1]:
                # Check that neurons are connected and not both present in one of the ensembles
                if self.conPN_PN[i,j] == 1 and (j not in self.ensembleNeurons[0]) and (i not in self.ensembleNeurons[1]):
                    tempConnMatrix[i,j] = True

    self.betweenWeights_Mean = np.average(self.weightPN_PN[:,tempConnMatrix],axis=1)
    

    #self.betweenWeights_SD = np.std(self.weightPN_PN[:,tempConnMatrix],axis=1)
    self.betweenWeights_SD = sem(self.weightPN_PN[:,tempConnMatrix],axis=1)
    if self.n_VIP == 2:
        name = [' A ', ' B ',' A ', ' B ']
    else:
        name = [' ',' ',' ',' ']
    # Plot the results...
    
    fig, ax = plt.subplots(figsize=(11,8))
    for VIP in range(self.n_VIP+self.n_randInputs):
    
        if VIP >= self.n_VIP:
            ax.plot(np.linspace(0,self.time_s, num = self.time_ms),self.withinWeights_Mean[VIP,:], label = 'within control' + name[VIP] + r'$\pm$ SEM', color = self.color[VIP])
        else:
            ax.plot(np.linspace(0,self.time_s, num = self.time_ms),self.withinWeights_Mean[VIP,:], label = 'within teacher' + name[VIP] + r'$\pm$ SEM', color = self.color[VIP])
        ax.fill_between(np.linspace(0,self.time_s, num = self.time_ms), self.withinWeights_Mean[VIP,:]-self.withinWeights_SD[VIP,:], self.withinWeights_Mean[VIP,:]+self.withinWeights_SD[VIP,:], color = self.color[VIP],alpha=0.3)
    
    # Plot the between weight evolution (not quite right)
    ax.plot(np.linspace(0,self.time_s, num = self.time_ms),self.betweenWeights_Mean, color = 'black',linestyle='dashed', label = r'between $\pm$ SEM')
    ax.fill_between(np.linspace(0,self.time_s, num = self.time_ms), self.betweenWeights_Mean-self.betweenWeights_SD, self.betweenWeights_Mean+self.betweenWeights_SD, color = 'black', alpha=0.3)
    ax.legend(loc="lower right",fontsize = 20, framealpha=0)
    ax.spines[['right', 'top']].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=22)
    ax.set_xlabel("time (s)",fontsize=30)
    ax.set_ylabel("average weight",fontsize=30)
    ax.set_ylim((0,2))
    yticks = ax.yaxis.get_major_ticks()
    yticks[-1].set_visible(False)


    plt.show()

    mpl.rcParams['path.simplify_threshold'] = 0.1111


def plotEnsembleStrength(self):

    # Generate lists to store the name of ensemble and if ensemlbes are trained or not.
    Ensembles = []
    Trained = []
    Activities = []
    Neuron = []


    col =  ['#98df8a','#2ca02c']
    # Create data frame for untrained examples.
    Activities = self.ensembleActivitesUntrained.copy() + self.ensembleActivites.copy()
    Neuron = self.ensembleNeurons.copy() + self.ensembleNeurons.copy() 
    Trained = [['untrained' for i in range(len(sublist))] for sublist in self.ensembleActivitesUntrained.copy()] + [['trained' for i in range(len(sublist))] for sublist in self.ensembleActivites.copy()]
    # This is a concat. of two very long (but identical) list comprehensions. Creates a list with the same dimensions as 'Activities' or 'Neuron' but stores if a teacher signal is present (VIP) or the random input is presented.
    

    Ensembles = [['teacher' for i in range(len(sublist[1]))] if (sublist[0] < len(self.ensembleActivitesUntrained.copy()) - 1) else ['control' for i in range(len(sublist[1]))] for sublist in enumerate(self.ensembleActivitesUntrained.copy()) ] \
    + [['teacher' for i in range(len(sublist[1]))] if (sublist[0] < len(self.ensembleActivites.copy()) - 1) else ['control' for i in range(len(sublist[1]))] for sublist in enumerate(self.ensembleActivites.copy())]


    # Uncomment if more than one teacher present!!!! And comment out two lines above!
    #Ensembles = [['teacher ' + str(sublist[0] + 1) for i in range(len(sublist[1]))] if (sublist[0] < len(self.ensembleActivitesUntrained.copy()) - 1) else ['no teacher' for i in range(len(sublist[1]))] for sublist in enumerate(self.ensembleActivitesUntrained.copy()) ] \
    #+ [['teacher ' + str(sublist[0] + 1) for i in range(len(sublist[1]))] if (sublist[0] < len(self.ensembleActivites.copy()) - 1) else ['no teacher' for i in range(len(sublist[1]))] for sublist in enumerate(self.ensembleActivites.copy())]


    # Create a data frame out of the lists
    df = pd.DataFrame({'activity': [item for sublist in Activities for item in sublist], 'neuron': [item for sublist in Neuron for item in sublist],\
     'ensemble': [item for sublist in Ensembles for item in sublist], 'trained': [item for sublist in Trained for item in sublist]})
    
    pd.set_option("display.max_rows", 100)
    

    


    # Plot

    fig, ax = plt.subplots(figsize=(12,8))
    sns.swarmplot(data=df, y="activity", x = "ensemble", hue = "trained",palette = col, dodge = True, ax=ax, size = 8 )	


    # Connect data points

    for i in range(len(self.ensembleActivites)):
        locs1 = ax.get_children()[i*2].get_offsets()
        locs2 = ax.get_children()[i*2+1].get_offsets()
        for j in range(locs1.shape[0]):
            x = [locs1[j, 0], locs2[j, 0]]
            y = [locs1[j, 1], locs2[j, 1]]
            ax.plot(x, y, color="black", alpha=0.3)
    ax.set_xlabel('')
    ax.set_ylabel('activity (rate)', fontsize=16)
    ax.legend(title='',fontsize = 14, loc = 'upper right')
    
    plt.tick_params(axis='both', which='major', labelsize=16)


    plt.show()

def plotWeightDistribution(self):

    # Extract all trained weights (disregard weights between neurons that are not connected...)
    weights = self.weightPN_PN[-1,self.conPN_PN.astype(bool)].flatten()
    weights0 =  self.weightPN_PN[0,self.conPN_PN.astype(bool)].flatten()
    
    
    log_weights = np.log(weights)
    log_weights0 = np.log(weights0)
    
    mymax = max([max(weights0),max(weights)])
    bin_list = np.linspace(0,mymax, num=100)
    
    mymin_log = min([min(log_weights0),min(log_weights)])
    mymax_log = max([max(log_weights0),max(log_weights)])
    
    bin_list_log = np.linspace(mymin_log,mymax_log, num=100)
    
    col =  ['#98df8a','#2ca02c']
    plt.figure(figsize=(12,8))
    plt.hist(weights0, bins = bin_list, density = True, color = 'gray', alpha = 0.6, label = "initialized")
    plt.hist(weights, bins = bin_list, density = True, color = col[1], alpha = 0.3, label = "trained")
    plt.xlabel('weight',fontsize=16)
    plt.ylabel('probability density',fontsize=16)
    #plt.title('Weight distribution')
    plt.legend(fontsize = 16)
    plt.tick_params(axis='both', which='major', labelsize=14)

    plt.show()
    
    plt.figure(figsize=(12,8))
    plt.hist(log_weights0, bins = bin_list_log, density = True, color = 'gray', alpha = 0.6, label = "initialized")
    plt.hist(log_weights, bins = bin_list_log, density = True, color = col[1] , alpha = 0.3, label = "trained")
    plt.xlabel('log(weight)',fontsize=16)
    plt.ylabel('probability density',fontsize=16)
    #plt.title('Weight distribution')
    plt.legend(fontsize = 16)
    plt.tick_params(axis='both', which='major', labelsize=14)

    plt.show()


def plotInput(self):

    time = np.linspace(0, self.time_s, num = self.time_ms)
    with plt.style.context('seaborn-v0_8-dark'):
        # Plot input
        

        fig = plt.figure()
        for i in range(int(self.time_ms / self.n_burst)):
            plt.hlines(np.where(self.input[:,i*self.n_burst]),i*self.n_burst,i*self.n_burst+self.n_burst, linewidth=1.2)
        plt.title("input")
        plt.xlabel("time (ms)")
        plt.ylabel("input index")
    plt.show()


