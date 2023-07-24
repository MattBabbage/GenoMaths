# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import graphviz

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def create_digraph(depth, width):
    clear_digraph = graphviz.Digraph('wide')
    for i in range(0, depth):
        for i in range(0, width):
            clear_digraph.edges(0)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    w = create_digraph(3,2)
    w = graphviz.Digraph('wide')
    w.edges(('0', str(i)) for i in range(1, 5))
    #doctest_mark_exe()
    w.view()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
