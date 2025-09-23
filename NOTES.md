
## Notes on Graciunias et al. 2016

$$ (V_{e+s}, n, m, n-m) $$
$$ V_{e+s} $$ (end systems and nodes)

n total number of queues
m number of scheduled queues
n-m queues remaining for BE traffic

(L c V x V)
duplex-link between nodes 
[v_a, v_b] e L, [v_b, v_a] e L

<[v_a, v_b].s, [v_a, v_b].d, [v_a, v_b].mt, [v_a, v_b].c>
s speed of the link in Mbs
d delay of the link (e.g. propagation or processing delay)
mt marcotick of the link (granularity of time differentation possible)
c number of available queues

critical streams S
s_i e S from sender v_a to receiver v_b
s_i = [[v_a, v_1], [v_1, v_2], ... , [v_n-1, v_n], [v_n, v_b]]
<s_i.e2e, s_i.L, s_i.T>
e2e maximum end-to-end latency allowed
L length of the stream (TODO: what that means?)
T period of the stream

s_i^[v_a, v_b].p assigned queue of instance of the stream

set of frame f_i,j^[v_a, v_b] of stream instance s_i^[v_a, v_b] by F_i^[v_a, v_b]
first frame is f_i,1^[v_a, v_b], last frames are last(F_i^[v_a, v_b])
<f_i,j^[v_a, v_b].phi, f_i,j^[v_a, v_b].T, f_i,j^[v_a, v_b].L>
phi e [0, f_i,j^[v_a, v_b].T] offset in macroticks
T = \ceiling{\frac{s_i.T}{[v_a, v_b].mt}} period of the stream scaled to marcoticks of the link
L = \ceiling{\frac{s_i.L \dot [v_a, v_b].s}{[v_a, v_b].mt}} transmission duration in macroticks

What do I need?
I need the number of total queues and scheduled queues.
I need the nodes and links of the network.
I need the speed, delay, marcotick and number of available queues on a link.
I need all streams to be processed.
I need the maximum end-to-end latency allowed, the length and the period of the streams.

What to solve for?
Solve for the assigned queue of the instance of the stream.
Solve for the offset (phi) of a all frames.

Constraints
Frame constraint
Each frame needs to be scheduled between 0 and the period of the stream substracted by the length of the transmission of the frame.

Link contraint
No two frames that are routed through the same egress port of a device may overlap in the time domain.

Stream Transmission Constraint
A frame of stream can only be scheduled if the respective frame on the previous link has been completly received.

End-to-End Constraint
The last frame should have been received before the maximum end-to-end latency was reached.

802.1Qbv Contraints
Choose between either
Stream Isolation Constraint

Frame Isolation Constraint