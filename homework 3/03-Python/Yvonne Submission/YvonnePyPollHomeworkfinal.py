# Module for reading CSV files
import csv
from os import write

#Set path for file, make sure to chnage backslashes 
csvpath = "03-Python/Yvonne Submission/election_data.csv"


#set my variables
total_votes = 0
#make candidates in a list form
candidates = []
#keep count of voted for each candidates starting from 0
candidate_votes = {"Khan":0, "Correy":0, "Li":0, "O'Tooley":0}

# Open the CSV
with open(csvpath, "r") as file:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(file, delimiter=',')

    # Looking at data set we know the first row is the Header and I want to skip it
    csvheader = next(csvreader)

     # Sanity Check:This prints just the header
    #print(csvheader)
    #print()

    # Start my loops
    for row in csvreader:
        # Calculate total votes = total number of lines within the election data. Adding one after each line
        total_votes = total_votes + 1

        # Complete list of candidates who received votes
        if row[2] not in candidates:
            candidates.append(row[2])

        #Calculate voted for candidates. If column 3 is candidates name them add a vote to their name. Using the list of canidates from code above
        if row[2] == "Khan":
            candidate_votes["Khan"] += 1
        elif row[2] == "Correy":
            candidate_votes["Correy"] += 1  
        elif row[2] == "Li":
            candidate_votes["Li"] += 1
        else:
            candidate_votes["O'Tooley"] += 1
    

print(total_votes)
print(candidates)
print(candidate_votes)

#Candidate vote results from above
khan = 2218231
correy = 704200
li = 492940
otooley = 105630

#find max value in my dictionary of candidates or inother words my winner
#https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary used this google reference
cand_winner = max(candidate_votes, key=candidate_votes.get)
cand_winner_votes = candidate_votes[cand_winner]

#the winner
print(cand_winner)
#the winners amount of votes
print(cand_winner_votes)

#make percents: candidate votes /total votes x 100
khan_percent = round((khan/total_votes)*100,2)
print(khan_percent)
correy_percent = round((correy/total_votes)*100,2)
print(correy_percent)
li_percent = round((li/total_votes)*100,2)
print(li_percent)
otooley_percent = round((otooley/total_votes)*100,2)
print(otooley_percent)



#creating my summary election result    
print("Election Results")
print("----------------------------")
print(f"Total Votes: {total_votes}")
print("----------------------------")
print(f"Khan: {khan_percent}% {khan}")
print(f"Correy: {correy_percent}% {correy}")
print(f"Li: {li_percent}% {li}")
print(f"O'Tooley: {otooley_percent}% {otooley}")
print("----------------------------")
print(f"Winner: {cand_winner}")




# making it print to .txt
summary = f"""Election Results
-------------------------
Total Votes: {total_votes}
-------------------------
Khan: {khan_percent}% {khan}
Correy: {correy_percent}% {correy}
Li: {li_percent}% {li}
O'Tooley: {otooley_percent}% {otooley}
-------------------------
Winner: {cand_winner}"""

#Check it prints correctly
#print(summary)

with open("PYPoll_Election_Results.txt","w") as file:
    file.write(summary)