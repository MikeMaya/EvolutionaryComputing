entrada = map(int, raw_input().split())
max1=entrada[0]
max2=0
for i in range (1, len(entrada)):
	if entrada[i] >= max1:
		max2=max1
		max1=entrada[i]
	elif entrada[i] >= max2:
		max2=entrada[i]
print "DOS MAX ",max1," ",max2