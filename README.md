# VSVS Scheduler
Project started October 2019

[`Authors`](docs/authors.txt)

**Description**: Imports data from `data/classrooms.csv`, `data/individuals.csv`, and `data/partners.csv`and assigns
 volunteers to groups. Outputs results in results/assignments.csv.

**For new IT Members**: [`Onboarding Guide`](docs/OnboardingNewITMembersx.md)
<hr>

## Getting Started

In order to run this program, you will first need to prepare three input files. Currently, these three input files
 come from the Google Forms we are using as the applications. Click on the following file names to get specifics
  about the specifications of each input file.
1. [`data/classrooms.csv`](data/classrooms.md)
2. [`data/individuals.csv`](data/individuals.md)
3. [`data/partners.csv`](data/partners.md)

<details><summary>Detailed Instructions on Generating Input Files</summary>
<p>

Before running:
  1. Export the responses to the individual application to csv and call it individuals.csv
  2. Export the responses to the partner application to csv and call it partners.csv
  3. Copy and paste (don't export) the classroom table from Access with headings and call it classrooms.csv (or manually collate responses from teacher sign up form)
  4. Place individuals.csv, partners.csv, and classrooms.csv into the data directory of this program

</p>
</details>

Assuming there are no deviations from the format outlined above, the program can be run through the main method in
 `src/main.py`. Assuming successful operations, there will be one output file generated: `results/assignments.csv
 `. If the `results/` directory does not exist, the program will create it for you.
 
**Note:** If you make any changes, be sure to add unit tests for any new code. Read [this documentation](data/automated_testing.md) for more information. Tests are run on each
commit through GitHub Actions. The badge at the top of this README tells us if tests are passing or failing.
 
## Repository Structure

This repository has/will have the following files:
```
- data/ (input csv files)
    - classrooms.csv
    - individuals.csv
    - partners.csv
- docs/
    - (various markdown files for more specific documentation)
- results/ (outputs generated from program)
    - assignments.csv
- src/
    - assign.py (functions for assigning volunteers, partners, drivers, etc)
    - classroom.py (contains the Classroom class)
    - convertSchedule.py (functions for creating schedule arrays and converting to military time)
    - globalAttributes.py (list of constants)
    - main.py (sorting algorithm, handle input + output files)
    - volunteer.py (contains the Volunteer class) 
```


## To-do
 
### For Fall 2020:
 
- [x] Write this documentation
- [x] switch the order of inputs
- [x] assign at least one in person volunteer to each group - David
- [x] substitute drivers with in-person
- [x] delete stuff that has to do with drivers
- [x] run sorting program and validate results

### Testing Metrics:
- [ ] people can make classrooms they're assigned to
- [ ] groups are assigned together
- [ ] each group has at least one in-person
- [ ] see how many groups of <MAX there are

### For the Future:

- [ ] sort robotics?
- [ ] add global constants + change methods so scheduling times collected can be changed in the future (like constants for start time (7:15), time period (15 min), and periods collected (34))
- [ ] group_number == -1 means unassigned
- [ ] how many passengers to consider someone a driver? currently if passengers >= MAX_TEAM_SIZE. highest option on form is 4+, so if we change MAX_TEAM_SIZE to 5, no one will ever be a driver
- [ ] optimize scheduling more by adding TRAVEL_TIME constants for every school
- [x] checking for duplicate submissions - if people fill out twice (On Google Form, limit to 1 response)
- [ ] do something if classroom is more than hour long
- [ ] make a teacher sign up form with better data input and data validation
- [ ] add a lot of unit tests

### Possible To-do:
- [ ] The phone numbers have different formats. We could use this [package](https://pypi.org/project/phonenumbers/) to parse phone numbers.
- [ ] Add type annotations/docstrings to specify the type for each attribute
 
 
