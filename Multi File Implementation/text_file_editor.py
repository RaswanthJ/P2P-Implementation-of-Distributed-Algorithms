def read_state(node_id):
    try:
        with open(f'n_{node_id}.txt', 'r') as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return None

def write_state(node_id, state):
    with open(f'n_{node_id}.txt', 'w') as file:
        file.write(str(state))
        
n=5
Array = [10,20,30,50,40]     #Fill the values that you want your nodes(Text files) to have before running the coordinator

for i in range(0,n):
    write_state(i+1,Array[i])
