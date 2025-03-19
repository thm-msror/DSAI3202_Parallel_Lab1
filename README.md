# DSAI 3202 – Parallel and Distributed Computing  
## Lecture 6 - Distributed Computing with Python

---

### Tutorial on mpi4py 
- Scatter is broadcasting or distributing: 
    - Rank 0 distributes the data (numbers and number) to all other processes or machines, and one process takes one number
- request.wait() waits for all the request to be done like thread.join()
- Difference between send, recv & isend, irecv:
    - send/recv: Blocking communication – the program waits until the data is sent/received before proceeding.
    - isend/irecv: Non-blocking communication – the program continues execution immediately after initiating the send/receive, allowing overlap of computation and communication. Use request.wait() to ensure completion.
---