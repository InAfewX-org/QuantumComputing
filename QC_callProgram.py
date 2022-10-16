#!/usr/bin/env python
# Author: KWC

# sample how to use it
# see my clonen : https://github.com/corbett/QuantumComputing
# and another js gui: https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22•%22],[%22•%22]]}


# under macos call idle3 under terminal
# may need to do command-A, ^5, <ret> then F5, <ret> 

from QuantumComputer import *
#from ibm_5q_full import * #from QuantumComputer.py

# put this file same directory as the main program e.g. 
# need to modify it match the source file program name
# and need to use import *

def myProgram(programCode,programMessage=""):

	print("--------------------------------------")
	print(programMessage)
	print("--------------------------------------")
	
	qc = QuantumComputer() 

	program_object=Program(programCode)

	qc.execute(program_object.code)

	for cubits in ["q0","q1","q2","q3","q4"]: #assume this
		on_qubit=qc.qubits.get_quantum_register_containing(cubits)
		# seems not work in pythonista
		# print(f"{cubits}:{on_qubit=}")
		print(f"\n{on_qubit.get_state()}\n") # may need to dig deeper

	qc.reset() # not need to redefine = QuantumComputer() 

	qc.execute(programCode)

	Probability.pretty_print_probabilities(qc.qubits.get_quantum_register_containing("q0").get_state())


if __name__ == '__main__':
	print("--start--ibm_5q_callProgram--")
	

	myProgram("""   h q[0];
			cx q[0], q[1];
			""","no Measure just H and CX")

	myProgram("""   h q[0];
			cx q[0], q[1];
			measure q[0];
			""","H and CX, measure |0>") # as entangled, measure one...

	myProgram("""   h q[0];
			cx q[0], q[1];
			measure q[1];
			""","H and CX, measure |1>")

	myProgram("""h q[0];
			cx q[0], q[1];
			measure q[0];
			measure q[1];
			""","H and CX, measure |0> |1>")

	myProgram("""   h q[0];
			cx q[0], q[1];
			cx q[0], q[1];
			h q[0];
			measure q[0];
			""","H and CX, measure |0> untangled?") # not really ...

	myProgram("""   h q[0];
			h q[1];
			x q[2];
			cx q[1], q[2];
			cx q[0], q[2];
			h q[0];
			h q[1];
			h q[2];
			""","Read me Sample 1") # readme sample 1


	myProgram("""   x q[2];
			cx q[1], q[2];
			h q[1];
			h q[2];
			cx q[1], q[2];
			h q[1];
			h q[2];
			cx q[1], q[2];
			measure q[1];
			measure q[2];
			""","Read me Sample 2") # readme sample 2 IBM ts IV p2


	
	
	print("--end--ibm_5q_callProgram--")


	print("--read me sample 1--")

	# from QuantumComputer import *

	ghz_example_code="""h q[0];
		h q[1];
		x q[2];
		cx q[1], q[2];
		cx q[0], q[2];
		h q[0];
		h q[1];
		h q[2];"""
	qc=QuantumComputer()
	qc.execute(ghz_example_code)
	Probability.pretty_print_probabilities(qc.qubits.get_quantum_register_containing("q0").get_state())

	print("--read me sample 2 note reset --")


	swap_example_code="""x q[2];
		cx q[1], q[2];
		h q[1];
		h q[2];
		cx q[1], q[2];
		h q[1];
		h q[2];
		cx q[1], q[2];
		measure q[1];
		measure q[2];"""
	qc.reset()
	qc.execute(swap_example_code)
	Probability.pretty_print_probabilities(qc.qubits.get_quantum_register_containing("q2").get_state())

	# Swap Qubits example IBM tutorial Section IV, Page 2
	qc=QuantumComputer()
	qc.apply_gate(Gate.X,"q2")
	qc.apply_two_qubit_gate_CNOT("q1","q2")
	qc.apply_gate(Gate.H,"q1")
	qc.apply_gate(Gate.H,"q2")
	qc.apply_two_qubit_gate_CNOT("q1","q2")
	qc.apply_gate(Gate.H,"q1")
	qc.apply_gate(Gate.H,"q2")
	qc.apply_two_qubit_gate_CNOT("q1","q2")
	qc.measure("q1")
	qc.measure("q2")
	Probability.pretty_print_probabilities(qc.qubits.get_quantum_register_containing("q1").get_state())

	# Swap Qubits example IBM tutorial Section IV, Page 2

	# likely need a qc= or qc.reset?

	qc.reset() #=QuantumComputer() # if on its own
	q1=State.zero_state
	q2=State.zero_state
	q2=Gate.X*q2
	new_state=Gate.CNOT2_01*np.kron(q1,q2)
	H2_0=np.kron(Gate.H,Gate.eye)
	H2_1=np.kron(Gate.eye,Gate.H)
	new_state=H2_0*new_state
	new_state=H2_1*new_state
	new_state=Gate.CNOT2_01*new_state
	new_state=H2_0*new_state
	new_state=H2_1*new_state
	new_state=Gate.CNOT2_01*new_state
	Probability.pretty_print_probabilities(new_state)
