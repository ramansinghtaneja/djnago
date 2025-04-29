const loadSheetJSScript = () => {
    const script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js";
    script.onload = () => {
        console.log("SheetJS loaded successfully.");
    };
    script.onerror = () => {
        console.error("Failed to load SheetJS.");
    };
    document.head.appendChild(script);
};

const loadjQuery = () => {
    const script = document.createElement('script');
    script.src = "https://code.jquery.com/jquery-3.6.0.min.js";
    script.onload = () => {
        console.log("jQuery loaded successfully.");
    };
    script.onerror = () => {
        console.error("Failed to load jQuery.");
    };
    document.head.appendChild(script);
};

// Function to load Bootstrap 4 (with jQuery)
const loadBootstrap4 = () => {
    // Load Popper.js for Bootstrap 4
    const popperScript = document.createElement('script');
    popperScript.src = "https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js";
    popperScript.onload = () => {
        console.log("Popper.js loaded successfully.");
    };
    popperScript.onerror = () => {
        console.error("Failed to load Popper.js.");
    };
    document.head.appendChild(popperScript);

    // Load Bootstrap 4 JS
    const bootstrap4Script = document.createElement('script');
    bootstrap4Script.src = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js";
    bootstrap4Script.onload = () => {
        console.log("Bootstrap 4 loaded successfully.");
    };
    bootstrap4Script.onerror = () => {
        console.error("Failed to load Bootstrap 4.");
    };
    document.head.appendChild(bootstrap4Script);
};

// Function to load Bootstrap 5 (without jQuery)
const loadBootstrap5 = () => {
    const bootstrap5Script = document.createElement('script');
    bootstrap5Script.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js";
    bootstrap5Script.onload = () => {
        console.log("Bootstrap 5 loaded successfully.");
    };
    bootstrap5Script.onerror = () => {
        console.error("Failed to load Bootstrap 5.");
    };
    document.head.appendChild(bootstrap5Script);
};

loadSheetJSScript();
loadjQuery();
loadBootstrap5(); 

document.getElementById('clearFilterBtn').addEventListener('click', function() {
   
    document.getElementById('filterForm').reset();
});
document.getElementById('filterForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const jobDescription = document.getElementById('jobDescription').value;
    const skills = document.getElementById('skills').value;
    const location = document.getElementById('location').value;
    const experience = document.getElementById('experience').value;

    const filterData = {
        skills: skills,
        location: location,
        experience: experience
    };

    const requestData = {
        job_description: jobDescription,
        filter_data: filterData
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/storepdf/profiles/filters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        if (response.ok && result.result) {
            displayCandidates(result.result);
            document.getElementById('generateExcelButton').style.display = 'block'; // Show the generate button
        } else {
            alert('No results found or error occurred.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('No data found.');
    }
});


const emailToPhoneNumber = {
    'suhanisjain23@gmail.com'  : '9766543210',
    'anandmanoj05@gmail.com'   : '9076543221',
    'marripatimadhav@gmail.com': '9886543232',
    'k.khare@outlook.com'      : '9870543232',
    'kaavyaakakj@gmail.com': '9176543232',
    'kanika.bansal.met20@itbhu.ac.in': '9976543232',
    'abdulateek36@gmail.com': '9876543232',
    'aayushsinghla@gmail.com': '9876543232',
    'it.amitagarwal@gmail.com': '9876543232',
    'viveksaha.arjun@gmail.com': '9876543232',
    'vinayravikanth@gmail.com' : '8234532211',
    'vaib_agarwal@yahoo.co.in' : '7634561111',
    'arya.vivek@gmail.com'  : '7676732334',
    'abhishek.ust@gmail.com' : '8432487874',
    'shreehari3@yahoo.com'    : '767676345366'
};


function displayCandidates(candidates) {
    const resultContainer = document.getElementById('result');
    resultContainer.innerHTML = ''; // Clear previous results

    candidates.forEach(candidate => {
        const phoneNumber = emailToPhoneNumber[candidate.email] || 'Phone number not available';

        const candidateCard = document.createElement('div');
        candidateCard.classList.add('candidate-card');

        const mydiv=document.createElement('div');

        const candidateName = document.createElement('h3');
        candidateName.textContent = candidate.full_name;

        const candidateEmail = document.createElement('p');
        candidateEmail.textContent = `Email: ${candidate.email}`;

        const candidatePhoneNumber = document.createElement('p');
        candidatePhoneNumber.textContent = `Phone: ${phoneNumber}`;

        const showDetailsButton = document.createElement('button');
        showDetailsButton.textContent = "Show Details";
        showDetailsButton.classList.add('btn', 'btn-sm', 'btn-primary','show_details_cs');
        
        // Create a div for holding the additional details
        const additionalDetailsDiv = document.createElement('div');
        additionalDetailsDiv.style.display = 'none';

        const candidateLocation = document.createElement('p');
        candidateLocation.textContent = `Location: ${candidate.location}`;

        const candidateSkills = document.createElement('p');
        candidateSkills.textContent = `Skills: ${candidate.technical_skills}`;

        const candidateExperience = document.createElement('p');
        candidateExperience.textContent = `Experience: ${candidate.experience}`;

        
        
       
        const candidateCheckbox = document.createElement('input');
        candidateCheckbox.type = 'checkbox';
        candidateCheckbox.value = candidate.email; // Use the candidate's email as a unique identifier
        candidateCheckbox.classList.add('candidate-checkbox');

        const screeningResultLabel = document.createElement('label');
        screeningResultLabel.textContent = "Screening Result";
        const screeningResultSelect = document.createElement('select');
        screeningResultSelect.classList.add('form-control');
        const resultOptions = ["Selected", "Rejected"];
        resultOptions.forEach(result => {
            const option = document.createElement('option');
            option.value = result;
            option.textContent = result;
            screeningResultSelect.appendChild(option);
        });

        // Score and Remarks fields (conditionally shown when 'Selected' is chosen)
        const scoreLabel = document.createElement('label');
        scoreLabel.textContent = "Score";
        const scoreInput = document.createElement('input');
        scoreInput.type = 'number';
        scoreInput.classList.add('form-control');
        scoreInput.style.display = 'none'; // Initially hide score input field

        const remarksLabel = document.createElement('label');
        remarksLabel.textContent = "Remarks";
        const remarksInput = document.createElement('textarea');
        remarksInput.classList.add('form-control');
        remarksInput.style.display = 'none'; // Initially hide remarks input field

        // Event listener to toggle score and remarks fields based on screening result
        screeningResultSelect.addEventListener('change', function () {
            if (screeningResultSelect.value === 'Selected') {
                scoreInput.style.display = 'block'; // Show score field when selected
                remarksInput.style.display = 'block'; // Show remarks field when selected
            } else {
                scoreInput.style.display = 'none'; // Hide score field when rejected
                remarksInput.style.display = 'none'; // Hide remarks field when rejected
            }
        }); 

        // Initially, default screening result is 'Rejected' and score/remarks are hidden
        screeningResultSelect.value = 'Rejected';
        scoreInput.style.display = 'none'; // Hide score initially
        remarksInput.style.display = 'none'; // Hide remarks initially


        const rowContainer = document.createElement('div');
        rowContainer.classList.add('row', 'g-3', 'mt-2');

        // Interview Status - Dropdown
        const interviewStatusCol = document.createElement('div');
        interviewStatusCol.classList.add('col-md-3'); // Each column takes up 4 spaces (out of 12)
        const interviewStatusLabel = document.createElement('label');
        interviewStatusLabel.classList.add('form-label', 'mb-1');
        interviewStatusLabel.textContent = "Interview Status";
        const interviewStatusSelect = document.createElement('select');
        interviewStatusSelect.classList.add('form-select', 'form-select-sm');
        const statusOptions = ["Pending", "Scheduled", "Completed"];
        statusOptions.forEach(status => {
        const option = document.createElement('option');
        option.value = status;
        option.textContent = status;
        interviewStatusSelect.appendChild(option);
        });
        interviewStatusCol.appendChild(interviewStatusLabel);
        interviewStatusCol.appendChild(interviewStatusSelect);

        // Interview Date
        const interviewDateCol = document.createElement('div');
        interviewDateCol.classList.add('col-md-3'); // Column size 4 for the date field
        const interviewDateLabel = document.createElement('label');
        interviewDateLabel.classList.add('form-label', 'mb-1');
        interviewDateLabel.textContent = "Interview Date";
        const interviewDateInput = document.createElement('input');
        interviewDateInput.type = 'date';
        interviewDateInput.classList.add('form-control', 'form-control-sm');
        interviewDateCol.appendChild(interviewDateLabel);
        interviewDateCol.appendChild(interviewDateInput);

        // Interview Time
        const interviewTimeCol = document.createElement('div');
        interviewTimeCol.classList.add('col-md-3'); // Column size 4 for the time field
        const interviewTimeLabel = document.createElement('label');
        interviewTimeLabel.classList.add('form-label', 'mb-1');
        interviewTimeLabel.textContent = "Interview Time";
        const interviewTimeInput = document.createElement('input');
        interviewTimeInput.type = 'time';
        interviewTimeInput.classList.add('form-control', 'form-control-sm');
        interviewTimeCol.appendChild(interviewTimeLabel);
        interviewTimeCol.appendChild(interviewTimeInput);

        // Append all columns to the row container
        rowContainer.appendChild(interviewStatusCol);
        rowContainer.appendChild(interviewDateCol);
        rowContainer.appendChild(interviewTimeCol);

// Append this row container to the candidate card






        const getSummaryButton = document.createElement('button');
        //getSummaryButton.textContent = "AI Insights";
        getSummaryButton.classList.add('btn', 'btn-sm', 'btn-primary', 'ms-auto','myinsights');
        const icon = document.createElement('i');
        icon.classList.add('bi', 'bi-lightbulb', 'me-1');

        // Append the icon and the text "AI Insights" to the button
        getSummaryButton.appendChild(icon);
        getSummaryButton.appendChild(document.createTextNode('AI Insights'));
        getSummaryButton.addEventListener('click', function() {
            // Collecting candidate's details
            const candidateData = {
                full_name: candidate.full_name,
                email: candidate.email,
                technical_skills: candidate.technical_skills,
                experience: candidate.experience,
               
            };

            // Get the job description
            const jobDescription = document.getElementById('jobDescription').value;

            const requestData = {
                job_description: jobDescription,
                candidate_data: candidateData
            };

            fetch('http://127.0.0.1:8000/storepdf/profiles/summary', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            })
            .then(response => {
                // Log the response to inspect it
                console.log('Response:', response);
            
                // Check if the response is OK before parsing
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
            
                // Parse the response as JSON and return it
                return response.json(); 
            })
            .then(data => {
                // Log the data to inspect the parsed result
                console.log('Data:', data);
            
                if (data && data.result) {
                   

                    // Check if positive_points and lacking_points exist in the data
                    const positivePoints = data.result.positive_points || 'No positive points available.';
                    const lackingPoints = data.result.lacking_points || 'No lacking points available.';
                    
                  
                    // Create HTML structure
                    let positivePointsHtml = '';
                    if (positivePoints) {
                        const positivePointsArray = positivePoints.split(' - ');
                        positivePointsHtml = '<div style="max-height: 200px; overflow-y: auto;">'; // Scrollable area for positive points
                        positivePointsHtml += '<ul>';
                        positivePointsArray.forEach(point => {
                            positivePointsHtml += `<li>${point.trim()}</li>`;
                        });
                        positivePointsHtml += '</ul></div>';
                    }
                
                    // Create scrollable container for lacking points
                    let lackingPointsHtml = '';
                    if (lackingPoints) {
                        const lackingPointsArray = lackingPoints.split(' - ');
                        lackingPointsHtml = '<div style="max-height: 200px; overflow-y: auto;">'; // Scrollable area for lacking points
                        lackingPointsHtml += '<ul>';
                        lackingPointsArray.forEach(point => {
                            lackingPointsHtml += `<li>${point.trim()}</li>`;
                        });
                        lackingPointsHtml += '</ul></div>';
                    }
                
                    // Combine both sections into the summary content
                    const summaryContent = `
                        <h2>${candidate.full_name}</h2>
                        <h4>Positive Points:</h4>
                        ${positivePointsHtml}
                        <hr>
                        <h4>Lacking Points:</h4>
                        ${lackingPointsHtml}
                    `;
                
                    // Insert the generated HTML into the modal content
                    document.getElementById('candidateSummaryContent').innerHTML = summaryContent;
                
                    // Show the modal with the candidate summary
                    $('#candidateSummaryModal').modal('show');
                    //alert("Candidate Summary: " + JSON.stringify(data.result));
                } else {
                    alert("No summary available for this candidate.");
                }
            })
            .catch(error => {
                // Catch and log any errors
                console.error('Error:', error);
                alert('An error occurred while fetching the candidate summary.');
            });
            
        });

        additionalDetailsDiv.appendChild(candidateLocation);
        additionalDetailsDiv.appendChild(candidateSkills);
        additionalDetailsDiv.appendChild(candidateExperience);
        additionalDetailsDiv.appendChild(rowContainer);

        showDetailsButton.addEventListener('click', function () {
            // Toggle visibility of additional details
            if (additionalDetailsDiv.style.display === 'none') {
                additionalDetailsDiv.style.display = 'block';
                showDetailsButton.textContent = "Hide Details"; // Change button text
            } else {
                additionalDetailsDiv.style.display = 'none';
                showDetailsButton.textContent = "Show Details"; // Change button text back
            }
        });

        candidateCard.appendChild(candidateName);
        candidateCard.appendChild(candidateEmail);
        candidateCard.appendChild(candidatePhoneNumber);
        candidateCard.appendChild(candidateCheckbox);
        candidateCard.appendChild(showDetailsButton);
        candidateCard.appendChild(getSummaryButton);
        candidateCard.appendChild(additionalDetailsDiv);
        resultContainer.appendChild(candidateCard);
    });
}

// New button for searching by job description
document.getElementById('searchByJobDescButton').addEventListener('click', async function() {
    const jobDescription = document.getElementById('jobDescription').value;

    if (!jobDescription.trim()) {
        alert('Please enter a job description to search.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/storepdf/profiles/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ job_description: jobDescription })
        });

        const result = await response.json();

        if (response.ok && result.result) {
            displayCandidates(result.result); // Display results similar to the other API
            document.getElementById('generateExcelButton').style.display = 'block'; // Show the generate button
        } else {
            alert('No results found or error occurred.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching the data.');
    }
});

// Function to generate Excel from selected candidates
document.getElementById('generateExcelButton').addEventListener('click', function() {
    const selectedCandidates = [];
    const checkboxes = document.querySelectorAll('.candidate-checkbox:checked');
    checkboxes.forEach(checkbox => {
        const candidateCard = checkbox.closest('.candidate-card');
        const email = candidateCard.querySelector('p').textContent.split(': ')[1];
        const phoneNumber = candidateCard.querySelector('p').nextElementSibling.textContent.split(': ')[1];
        const interviewStatus = candidateCard.querySelector('select').value;
        const interviewDate = candidateCard.querySelector('input[type="date"]').value;
        const interviewTime = candidateCard.querySelector('input[type="time"]').value;

        const interviewLink = 'http://localhost:5173/';
        
        selectedCandidates.push({
            full_name: candidateCard.querySelector('h3').textContent,
            email: email,
            phone_number: phoneNumber, 
            interview_status: interviewStatus,
            interview_date: interviewDate,
            interview_time: interviewTime,
            interview_link: interviewLink
            
        });
    });

    if (selectedCandidates.length > 0) {
        // Send selected candidates data to server to generate Excel
        generateExcel(selectedCandidates);
    } else {
        alert('Please select candidates for the Excel export.');
    }
});
// Function to toggle visibility of the div
document.getElementById('shortlist-button').addEventListener('click', function(event) {
event.preventDefault();  // Prevent default link behavior (if any)

// Get both div elements
var shortlistDiv = document.getElementById('shortlist-div');
var shortlistDivHm = document.getElementById('shortlist-div-hm');

// Hide both divs first
shortlistDiv.style.display = 'none';
shortlistDivHm.style.display = 'none';

// Show the specific div based on the clicked button
if (shortlistDiv.style.display === 'none' || shortlistDiv.style.display === '') {
shortlistDiv.style.display = 'block';  // Show the div for shortlist-button
}
});


 
document.getElementById('hm-button').addEventListener('click', function(event) {
event.preventDefault();  // Prevent default link behavior (if any)

// Get both div elements
var shortlistDiv = document.getElementById('shortlist-div');
var shortlistDivHm = document.getElementById('shortlist-div-hm');

// Hide both divs first
shortlistDiv.style.display = 'none';
shortlistDivHm.style.display = 'none';

// Check if any candidate is selected
const checkboxes = document.querySelectorAll('.candidate-checkbox:checked');
if (checkboxes.length > 0) {
// Array to store selected candidates' details
const selectedCandidates = [];

checkboxes.forEach(checkbox => {
    const candidateCard = checkbox.closest('.candidate-card');
    const candidateName = candidateCard.querySelector('h3').textContent; // Get candidate name
    const email = candidateCard.querySelector('p').textContent.split(': ')[1];
    const phoneNumber = candidateCard.querySelector('p').nextElementSibling.textContent.split(': ')[1];
    const interviewStatus = candidateCard.querySelector('select').value;
    const interviewDate = candidateCard.querySelector('input[type="date"]').value;
    const interviewTime = candidateCard.querySelector('input[type="time"]').value;

    // Push candidate details to the array
    selectedCandidates.push({
        name: candidateName,
        email: email,
        phone: phoneNumber,
        interviewStatus: interviewStatus,
        interviewDate: interviewDate,
        interviewTime: interviewTime
    });
});

// Prepare the HTML content to be displayed
const copiedContentDiv = document.getElementById('copied-content');
copiedContentDiv.innerHTML = ''; // Clear any previous content in shortlist

// Generate HTML for each candidate in the array and insert it at once
selectedCandidates.forEach(candidate => {
    const candidateHTML = `
        <div class="candidate-summary">
            <h4>${candidate.name}</h4>
            <p>Email: ${candidate.email}</p>
            <p>Phone: ${candidate.phone}</p>
            
        </div>
    `;
    copiedContentDiv.insertAdjacentHTML('beforeend', candidateHTML); // Append the candidate's HTML
});

// Show the shortlist div with the selected candidates
shortlistDivHm.style.display = 'block';
} else {
alert('Please select candidates before proceeding.');
}
}); 





document.addEventListener('DOMContentLoaded', function () {
    const scheduleButtonContainer = document.createElement('div');
    scheduleButtonContainer.classList.add('text-center');
    const scheduleInterviewButton = document.createElement('button');
    scheduleInterviewButton.textContent = 'Schedule Interview';
    scheduleInterviewButton.id = 'scheduleInterviewButton';
    scheduleInterviewButton.classList.add('btn', 'btn-primary', 'w-100', 'mt-4');
    scheduleButtonContainer.appendChild(scheduleInterviewButton);
    //document.getElementById('resul').appendChild(scheduleButtonContainer);

    // Add the event listener for the "Schedule Interview" button after it is in the DOM
   // {% comment %} document.getElementById('scheduleInterviewButton').addEventListener('click', function () {
      //  const selectedCandidates = [];
   //     const checkboxes = document.querySelectorAll('.candidate-checkbox:checked');
   //     const jobDescription = document.getElementById('jobDescription').value;

    //    if (!jobDescription) {
   //         alert('Please provide a job description.');
   //         return;
    //    }

     //   checkboxes.forEach(checkbox => {
     //       const candidateCard = checkbox.closest('.candidate-card');
    //        const interviewStatus = candidateCard.querySelector('select').value;

            // Only consider candidates whose interview status is "Scheduled"
       //     if (interviewStatus === 'Scheduled') {
         //       const email = candidateCard.querySelector('p').textContent.split(': ')[1];
                 // Assuming this is the job description field
          //      const score = candidateCard.querySelector('input[type="number"]').value; // Getting the score
           //     const remarks = candidateCard.querySelector('textarea').value; // Getting the remarks

         //       selectedCandidates.push({
         //           email: email,

        //            score: score,
     //               remarks: remarks
          //      });
          //  }
      //  });

        // If no candidates are selected, show an alert
   //     if (selectedCandidates.length === 0) {
      //      alert('Please select candidates with "Scheduled" status for interview.');
      //      return;
     //   } 
        
      //  const requestBody = {
      //      job_description: jobDescription, // Include job description
      //      candidates: selectedCandidates   // Include selected candidates
       // };


        // Send the selected candidates' data via POST request
     //   fetch('http://127.0.0.1:8000/storepdf/shortlist/', {
        //    method: 'POST',
         //   headers: {
          //      'Content-Type': 'application/json'
        //    },
       //     body: JSON.stringify(requestBody)
     //   })
          //  .then(response => response.json())
           // .then(data => {
       //         if (data.message) {
            //        alert('Selected candidates have been scheduled for interview.');
            //    } else {
         //           alert('Error occurred while scheduling interviews.');
              //  }
       //     })
      //      .catch(error => {
             //   console.error('Error:', error);
         //       alert('An error occurred while sending the request.');
         //   });
   // }); {% endcomment %}
});


        // Function to generate the Excel file
function generateExcel(candidates) {
    const XLSX = window.XLSX;

    const ws = XLSX.utils.json_to_sheet(candidates);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Candidates");

    // Export the file
    XLSX.writeFile(wb, "candidates.xlsx");
}



document.addEventListener('DOMContentLoaded', function () {
const selectJD = document.getElementById('select-jd');
const textarea = document.getElementById('jobDescription');
const clearBtn = document.getElementById('clear-jd');

// When user selects from dropdown
selectJD.addEventListener('change', function () {
const selectedValue = this.value;
if (selectedValue) {
textarea.value = selectedValue;
}
});

// When user clicks "clear" button
clearBtn.addEventListener('click', function () {
selectJD.selectedIndex = 0;
textarea.value = '';
});
});
