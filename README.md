# Organisation Chart Traversal

### Daniella Tobit 2022
<br />

<h2>🛠️ Installing and running instructions:</h2>

<p>1. Clone the repository</p>

```
git clone https://github.com/daniella-git/org-chart-traversal.git
```

<p>2. Navigate to directory</p>

```
cd org-chart-traversal
```

<p>3. Run the program</p>

```
python organisation_chain.py "<path to employee data file>" "<employee 1>"  "<employee 1>"
```

*For example:*
```
python organisation_chain.py "hierarchy_tree.txt" "Batman" "Super Ted"
```

<p>4. Run the tests</p>

```
python test_organisation_chain.py 
```

<br />
<h2>Program features</h2>

*   Reads and parses a file's data 
*   Finds the chain between two given employees via their managers
*   Identifies the lowest common ancestor between the two employees
*   Prints the shortest path of communication between the two employees that follows the organisation's hierarchy
