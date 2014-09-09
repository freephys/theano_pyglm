"""
Plotting for ROC curves and link prediction tests
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial

def plot_roc_curve(tprs, fprs, color='k', ax=None, subsample=1, label=None):
    """ Plot an ROC curve for the given true and false positive rates.
        If multiple rates are given, e.g. corresponding to multiple
        networks inferred using the same procedure, compute error bars
        (both horizontal and vertical) for the ROC curve.

        Plot in specified color, default black.

        Plot on the specified axes, or create a new axis necessary.
        
        Subsample allows you to subsample the errorbar
    """
    if ax is None:
        plt.figure(frameon=False)
        ax = plt.subplot(111)

    if not isinstance(tprs, list):
        tprs = [tprs]
    if not isinstance(fprs, list):
        fprs = [fprs]

    # Make sure all tprs and fprs are the same length
    N = tprs[0].size
    for (i,tpr) in enumerate(tprs):
        if not tpr.size == N:
            raise Exception("All TPRs must be vectors of length %d." % N)
        tprs[i] = tpr.reshape((N,1))
    for (i,fpr) in enumerate(fprs):
        if not fpr.size == N:
            raise Exception("All FPRs must be vectors of length %d." % N)
        fprs[i] = fpr.reshape((N,1))

    # Stack tprs and fprs to make matrices
    tprs = np.concatenate(tprs, axis=1)
    fprs = np.concatenate(fprs, axis=1)

    # Compute error bars (for both tpr and fpr)
    mean_tprs = np.mean(tprs, axis=1)
    std_tprs = np.std(tprs, axis=1)

    mean_fprs = np.mean(fprs, axis=1)
    std_fprs = np.std(fprs, axis=1)

    # Plot the error bars
    # plt.errorbar(mean_fprs, mean_tprs,
    #              xerr=std_fprs, yerr=std_tprs,
    #              ecolor=color, color=color,
    #              axes=ax)
    err = np.concatenate([np.array([mean_fprs-std_fprs, mean_tprs+std_tprs]).T,
                          np.flipud(np.array([mean_fprs+std_fprs, mean_tprs-std_tprs]).T)])
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path

    plt.gca().add_patch(PathPatch(Path(err),
                                  facecolor=color,
                                  alpha=0.5,
                                  edgecolor='none',
                                  linewidth=0))
    # plt.plot(err[:,0], err[:, 1],
    #          linestyle='--',
    #          color=color)

    plt.plot(mean_fprs, mean_tprs,
             linestyle='-',
             color=color,
             linewidth=2,
             label=label)

    # Plot the random guessing line
    plt.plot([0,1],[0,1], '--k')

    #plt.legend(loc='lower right')

    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.xlim((-0.01,1))
    plt.ylim((0.0,1))

    return ax
