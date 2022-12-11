input_str = "geeksforgeeks"

def sort_string(input_str):

	input_list = list(input_str)
	# Default output list is ["g"]
	output_list = [input_list.pop(0)]

	for i in range(len(input_list)):
		for j in range(len(output_list)):

			if ord(input_list[i]) < ord(output_list[j]):
				
				output_list.insert(j, input_list[i])

				break

		else:
			output_list.append(input_list[i])

	output_str = "".join(output_list)

	return output_str

sort_string(input_str)

# Time complexity of this algorithm can be O(n ** 2)

