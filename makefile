all:
	$ pip install -r requirements.txt
	$ gcc -o gps exec.c

install:
	$ pip install -r requirements.txt
	$ gcc -o gps exec.c
clean:
	$ rm !("__pycache__" | "env" | "nlp.py" | "text.txt" | "trash" | "build" | "gps.py" | "result.py" | "tokenizer.py" | "exec.c")	

test:
	$ ./gps -o ./testcases/testfile1.txt testfile1.py
	$ ./gps -o ./testcases/testfile2.txt testfile2.py
	$ ./gps -o ./testcases/testfile3.txt testfile3.py
