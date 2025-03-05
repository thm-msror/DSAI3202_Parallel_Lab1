from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    # Process 0 sends a non-blocking message to Process 1
    data_to_send = "Hello from Process 0"
    request = comm.isend(data_to_send, dest=1, tag=100)
    # Process 0 can perform other work here while the send operation completes
    request.wait()  # Wait for the non-blocking send to complete
    print("Process 0 sent data")
    
elif rank == 1:
    # Process 1 sets up a non-blocking receive from Process 0
    request = comm.irecv(source=0, tag=100)
    data_received = request.wait()  # Wait for the non-blocking receive to complete
    # 'status' object contains information about the received message
    status = request.Get_status()
    print("Process 1 received data: ", data_received)
    print("Status of the received message: ", status)