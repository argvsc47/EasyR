"""
mincol:arg
plscol:arg,arg
rencol:arg,arg
srtrow:arg,arg
minrow:arg (index)
plsrow:args (list of args only first slots use tho) plsrow:["client = someDood7", "id = 5"]
reocol:args #reocol:["b","c","a"]
merge:arg #merge:arg.csv
observe:5
"""

def mincol(arg):
	return f"""df <- df %>%\n\tselect(-{arg})"""

def plscol(arg,arg2):
	return f"""df${arg}={arg2}"""

def rencol(arg,arg2):
	return f"""df <- df %>%\n\trename({arg2} = {arg})"""

def srtrow(arg,arg2):
	if arg2 == "-":
		return f"""df <- df %>%\n\tarrange(desc({arg}))"""
	return f"""df <- df %>%\n\tarrange({arg})"""

def minrow(arg):
	return f"""df <- df %>%\n\tslice(-c({arg}))"""

def plsrow(args):
	rsy = f"""df <- df %>%\n\tadd_row("""
	ins = ""
	for arg in args:
		if args.index(arg) != len(args) - 1:
			ins += arg + ", "
		else:
			ins += arg
	rsy += ins + ")"
	return rsy

def reocol(args):
	return f"""df <- df[,{"c" + str(args).replace("[","(").replace("]",")")}]"""

def merge(arg):
	return f"""d2 <- read.csv({arg})\ndf <- merge(df, d2)"""

def observe(arg):
	return f"""head(df,{arg})"""

def Parser(sett,script):
	r = "{r}"
	lines = script.split("\n")
	rs = []
	for line in lines:
		ist = line.split(":")[0]
		ags = line.split(":")[1]
		rc = eval(ist + "(" + ags + ")", globals(), locals())
		rs.append(rc)
	rs = "\n".join(rs)
	R_output = f"""---
title: "Routput"
output: html_document
---
```{r}
library(dplyr)
df <- read.csv("{sett}")
{rs}
```
"""
	f = open("notebook.Rmd", "w")
	f.write(R_output)
	f.close()

def compile():
	os.system('Rscript generate.r')

import sys, os

cmd = sys.argv #tidyset data.csv script.td

cmd.pop(0)

print("Tidying dataset...")
scf = open(cmd[1], "r")
sc = scf.read()
scf.close()
Parser(cmd[0],sc)
compile()
print(f"Tidying Complete ! checkout your files: {cmd[0]} | notebook.Rmd | notebook.html")
