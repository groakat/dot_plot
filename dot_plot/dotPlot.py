import numpy as np
import pylab as plt

def generatePlotValues(x, width=3, space=0.1):
    
    vs = space# / 3.0
    vos = ((width - 1) / 2.0 - 1) * space
    
    if not x[0] == 0:    
        if x[0] % 2 == 0:
            ret = [[i * vs - vos for i in range(width)], [space / 2.0 for i in range(width)]]
            os = space / 2.0
            k = 1
        else:        
            ret = [[i * vs - vos for i in range(width)], [0 for i in range(width)]]
            os = 0
            k = 0
                        
        for m in range(1, x[0]):
            ret[0] += [i * vs - vos for i in range(width)]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k for i in range(width)]
            k += 1
        
        if x[1] == 1:
            ret[0] += [1 * vs]
            k += 1
            ret[1] += [(space * (k / 2 + 1) - os) * abs((-1)**(k))]
            
        if x[1] == 2:
            ret[0] += [1 * vs]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            k += 1
            ret[0] += [1 * vs]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            
        if x[1] == 3:
            ret[0] += [1 * vs]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            k += 1
            ret[0] += [1 * vs - space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            ret[0] += [1 * vs + space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            
        if x[1] == 4:
            ret[0] += [1 * vs - space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            ret[0] += [1 * vs + space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            k += 1
            ret[0] += [1 * vs - space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            ret[0] += [1 * vs + space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            
            
    else:
        if x[1] == 1:
            ret = [[1 * vs], [0]]  
        elif x[1] == 2:
            ret = [[1 * vs, 1 * vs],
                   [space / 2.0, -space / 2.0]]
        elif x[1] == 3:
            k = 0
            os = space / 2.0
            ret = [[1 * vs],
                   [(space * (k / 2 + 1) - os)  * (-1)**k]]
            k += 1
            ret[0] += [1 * vs - space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            ret[0] += [1 * vs + space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            
        elif x[1] == 4:
            k = 0
            os = space / 2.0
            ret = [ [1 * vs - space / 2.0],
                    [(space * (k / 2 + 1) - os)  * (-1)**k]]
            ret[0] += [1 * vs + space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            k += 1
            ret[0] += [1 * vs - space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
            ret[0] += [1 * vs + space / 2.0]
            ret[1] += [(space * (k / 2 + 1) - os)  * (-1)**k]
        
    return ret
      
def generateDotPlot(data, space=0.1, os=0, width=3):
    """
    Args:
        data (np.ndarray)
                each column is one column in the plot
        space (float)
                spacing between dots (horizontal and vertical)
        os (float)
                vertical offset of the entire plot
        kwargs (dict)
                kwargs of matplotlib scatter function
    """

    xs = []
    ys = []

    if len(data.shape) == 2:
        rng = range(data.shape[1])
    else:
        rng = [0]
        data = data.reshape(data.shape[0], 1)
    

    for c in rng:
        # hist = np.histogram(d[i], bins=5, range=(1,6))
        hist = np.histogram(data[:,c], bins=5, range=(1,6))

        plotRawVal = [[x/width, x % width] for x in hist[0]]
        
        for i in range(len(plotRawVal)):
            if not plotRawVal[i] == [0,0]:
                print plotRawVal[i]
                val = generatePlotValues(plotRawVal[i], width=width)

                xs += [x - space + os for x in val[0]]
                ys += [x + (i + 1) for x in val[1]]
            # plt.scatter(x=[x - space + os for x in val[0]], y=[x + (i + 1) for x in val[1]], **kwargs)


        os += c*2

    # plt.scatter(x=xs, y=ys, **kwargs)
    return xs, ys

      
def plotDotPlot(h, space=0.1, os=0, width=3, **kwargs):
    """
    Args:
        h (np.hist)
                histogram generated by np.hist
        space (float)
                spacing between dots (horizontal and vertical)
        os (float)
                vertical offset of the entire plot
        kwargs (dict)
                kwargs of matplotlib scatter function
    """
    
    plotRawVal = [[x/width, x % width] for x in h[0]]
    
    for i in range(len(plotRawVal)):
        if not plotRawVal[i] == [0,0]:
            print plotRawVal[i]
            val = generatePlotValues(plotRawVal[i], width=width)
            plt.scatter(x=[x - space + os for x in val[0]], y=[x + (i + 1) for x in val[1]], **kwargs)


def plot_matplot_lib(df, show=False):

    header = list(df.columns.values)

    fig = plt.figure(figsize=(df.shape[1] * 2 + 2, 12))  
    xs, ys = generateDotPlot(np.asarray(df), space=0.15, width=5)

    x = [[i*2, h] for i, h in enumerate(header)]

    plt.scatter(x=xs, y=ys, facecolors='black',marker='o', s=15)


    plt.axes().set_aspect('equal')
    plt.axes().set_autoscale_on(False)
    plt.axes().set_ybound(0,6)
    plt.axes().set_xbound(-0.9, len(header) * 2 + 0.9)
    
    plt.xticks(zip(*x)[0], zip(*x)[1] )
    plt.yticks(range(1,6))
    
    for tick in plt.axes().get_xaxis().get_major_ticks():
        tick.set_pad(15)
        tick.label1 = tick._get_text1()
        
    for tick in plt.axes().get_yaxis().get_major_ticks():
        tick.set_pad(15)
        tick.label1 = tick._get_text1()
        
    plt.setp(plt.xticks()[1], rotation=20)

    if show:
        plt.show()

    return fig


def save_xlsx(df, filename):
    import xlsxwriter
    import string

    header = list(df.columns.values)


    workbook = xlsxwriter.Workbook('chart.xlsx')
    worksheet = workbook.add_worksheet()

    # Create a new Chart object.
    chart = workbook.add_chart({'type': 'scatter'})

    # Write some data to add to plot on the chart.
    # data = [
    #     [1, 2, 3, 4, 5],
    #     [2, 4, 6, 8, 10],
    #     [3, 6, 9, 12, 15],
    # ]

    for c in range(len(header)):
        xs, ys = generateDotPlot(np.asarray(df.ix[:,c]), os=c*2, space=0.15, width=5)
        x_column = string.uppercase[c * 2]
        y_column = string.uppercase[c * 2 + 1]

        worksheet.write_column('{}1'.format(x_column),
                               xs)
        worksheet.write_column('{}1'.format(y_column),
                               ys)

        # Configure the chart. In simplest case we add one or more data series.
        chart.add_series({'categories': '=Sheet1!${c}$1:${c}${e}'.format(c=x_column,
                                                                     e=len(xs)),
                          'values': '=Sheet1!${c}$1:${c}${e}'.format(c=y_column,
                                                                     e=len(ys)),
                          'data_labels': {'legend_key': header[c]}})


    worksheet.write_column('{}1'.format(string.uppercase[len(header) * 2]),
                               header)


    # chart.set_legend({'position': 'none'})
    # chart.set_x_axis({'visible': False})
    chart.set_y_axis({'interval_unit': 1,
                      'major_unit': 1,
                      'minor_unit': 0,
                      'min':0})


    # Insert the chart into the worksheet.
    worksheet.insert_chart('{}7'.format(string.uppercase[len(header) * 2 + 1]), chart)

    workbook.close()


def save_plot(xs, ys, header, filename):
    fig = plot_matplot_lib(xs, ys, header, show=False)
    fig.savefig(filename, dpi=300, format=filename.split('.')[-1])


def read_csv(filename):    
    import os, io
    import pandas as pd

    df = pd.read_csv(filename)

    return df


# def plot_file(filename):
#     import os, io
#     import pandas as pd
#     print "plotting"
    
#     with io.open(filename, 'r') as f:
#         # header = f.readline().strip('\n').split('\t')
#         # a = np.genfromtxt(f, delimiter='\t', missing_values='')
#         df = pd.read_csv(filename, delimiter='\t')
#         header = list(df.columns.values)

                    
#     # d =  zip(*a)
#     x = []
#     fig = plt.figure(figsize=(df.shape[1] * 2 + 2, 12))    

#     xs, ys = generateDotPlot(np.asarray(df), space=0.15, width=5)


#     for i in range(df.shape[1]):
#         # hist = np.histogram(d[i], bins=5, range=(1,6))
#         # hist = np.histogram(df.ix[:,i], bins=5, range=(1,6))
#         # plotDotPlot(hist, space=0.15, os=i*2, width=5, facecolors='black',marker='o', s=15)
#         x += [[i*2, header[i]]]
        
#     plt.axes().set_aspect('equal')
#     plt.axes().set_autoscale_on(False)
#     plt.axes().set_ybound(0,6)
#     plt.axes().set_xbound(-0.9, i* 2 + 0.9)
    
#     plt.xticks(zip(*x)[0], zip(*x)[1] )
#     plt.yticks(range(1,6))
    
#     for tick in plt.axes().get_xaxis().get_major_ticks():
#         tick.set_pad(15)
#         tick.label1 = tick._get_text1()
        
#     for tick in plt.axes().get_yaxis().get_major_ticks():
#         tick.set_pad(15)
#         tick.label1 = tick._get_text1()
        
#     plt.setp(plt.xticks()[1], rotation=20)

#     plt.show()
        
    
    
