import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# def get_model_info(model_file_name):
#     model_info = open(model_file_name, 'r')
#     line_c = 0
#     model_name = ''
#     optimiser = ''
#     epochs = 0
#     batch_size = 0
#     learning_rate = 0.0
#     momentum = 0.0
#     for line in model_info.readlines():
#         line_c += 1
#         one_line = line.rstrip('\n')
#         if line_c == 2:
#             model_name = one_line.rstrip('(')
#         elif one_line.startswith("Optimizer"):
#             elements = one_line.split(' ')
#             optimiser = elements[1]
#         elif one_line.startswith("Epochs"):
#             elements = one_line.split(' ')
#             epochs = int(elements[1])
#         elif one_line.startswith("Size of batches:"):
#             elements = one_line.split(' ')
#             batch_size = int(elements[3])
#         elif one_line.startswith("Learning rate"):
#             elements = one_line.split(' ')
#             learning_rate = float(elements[2])
#         elif one_line.startswith("Momentum"):
#             elements = one_line.split(' ')
#             momentum = float(elements[1])
#     return model_name, optimiser, epochs, batch_size, learning_rate, momentum


def get_losses(data_file):

    results = open(data_file, 'r')
    training = []
    testing = []
    recall = 0.0
    precision = 0.0
    cpt = 0
    for line in results.readlines():
        if line.startswith("Epoch: "):
            if line.split(" ")[2].startswith("Loss:"):
                training.append(float(line.split(" ")[3]))
            elif line.split(" ")[2].startswith("ValidationLoss:"):
                testing.append(float(line.split(" ")[3]))

    return training, testing
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plots graphs from the PPI results.')
    parser.add_argument('-f', type=str, help='data file (without _loss)')
    parser.add_argument('-s', type=str, help='name for save of figure')

    args = parser.parse_args()
    data = args.f
    # data_model = args.f
    # data = data_model + "_loss"

    save = args.s
    if save is None:
        # save = data_model + ".png"
        save = data + ".png"

    #recover infos from model
    # model_name, optimiser, epochs, batch_size, learning_rate, momentum = get_model_info(data_model)

    # graph_title = "{} with {} optimiser, {} learning rate and {} batch size".format(model_name, optimiser, learning_rate, batch_size)
    graph_title = data
    
    training, testing = get_losses(data)
    epochs = len(training)
    
    t = np.linspace(0, epochs, num=epochs)

    fig, ax = plt.subplots()
    #ax.plot(t, training, testing)
    line, = ax.plot(t, training, label ="Training loss")
    line2, = ax.plot(t, testing, label ="Testing loss")
    ax.legend()
    
    ax.set(xlabel='epochs', ylabel='loss',
           title=graph_title)
    #if no file name has been defined, use model name

    fig.savefig(save)
        
    plt.show()
