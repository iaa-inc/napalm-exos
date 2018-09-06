Value port_number (\d+:?\d+?)
Value display_string ([^ ][^ ]{0,20})
Value description_string (..*)

Start
	# Full Record
	^${port_number}\s{3,6}${display_string}\s{0,20}\s{2}${description_string} -> Record
	# Missing Description-String
	^${port_number}\s{3,6}${display_string} -> Record
	# Missing Display String
	^${port_number}\s{3,6}\s{20}\s{2}${description_string} -> Record
	
