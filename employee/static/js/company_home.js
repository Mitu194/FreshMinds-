function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    selectedSection.classList.add('active');

    // Add active class to the clicked tab
    const selectedTab = document.querySelector(`a[href="#${sectionId}"]`);
    selectedTab.classList.add('active');
}

// Redirect to the About section
function redirectToAbout() {
    showSection('about');
}

function redirectToPosts() {
    // Hide all sections
    document.querySelectorAll(".content-section").forEach(section => section.classList.remove("active"));

    // Show the "Posts" section
    document.getElementById("posts").classList.add("active");

    // Update active tab
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector("[href='#posts']").classList.add("active");
}

function redirectToJobs() {
    // Hide all sections
    document.querySelectorAll(".content-section").forEach(section => section.classList.remove("active"));

    // Show the "Jobs" section
    document.getElementById("jobs").classList.add("active");

    // Update active tab
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector("[href='#jobs']").classList.add("active");
}

//post page back to home button code
 //function goBack()
// {
  //  window.location.herf='C:\project\desgin\rough73.html';
 //}
 const tabs = document.querySelectorAll('.nav-tabs .tab');

 // Check for the current URL to set the active tab (useful for navigation)
 const currentPath = window.location.pathname;
 
 // Function to dynamically set active tab
 function setActiveTab() {
     tabs.forEach(tab => {
         const href = tab.getAttribute('href');
         if (currentPath.includes(href)) {
             tab.classList.add('active');
         } else {
             tab.classList.remove('active');
         }
     });
 }
 
 // Add click listener to update active class without relying on URL
 tabs.forEach(tab => {
     tab.addEventListener('click', function (e) {
         tabs.forEach(t => t.classList.remove('active')); // Remove active class from all tabs
         this.classList.add('active'); // Add active class to the clicked tab
     });
 });
 
 // Set active tab based on the current URL (important for page reloads)
 setActiveTab();

 //job page::
 // Example: Updating job count dynamically
const jobCountElement = document.getElementById('job-count');
const totalJobs = 9057;

document.addEventListener('DOMContentLoaded', () => {
    jobCountElement.textContent = totalJobs.toLocaleString();
});

function navigateToJob(jobTitle) {
    // Create a URL parameter to pass the job title (optional)
    const jobPageUrl = `linkjob.html?title=${encodeURIComponent(jobTitle)}`;
    window.location.href = jobPageUrl;
}

document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.nav-tabs .tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', (event) => {
            event.preventDefault();
            const targetPage = tab.getAttribute('href');
            if (targetPage) {
                window.location.href = targetPage;
            }
        });
    });
});


//SEARCH FUNCTIONAKITY

document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.querySelector(".search-bar button");
  const searchInput = document.querySelector(".search-bar input");
  const jobCards = document.querySelectorAll(".job-card");

  searchButton.addEventListener("click", function () {
      const query = searchInput.value.toLowerCase();
      
      jobCards.forEach(job => {
          const jobTitle = job.querySelector("h4").textContent.toLowerCase();
          const jobLocation = job.querySelector("p:nth-child(4)").textContent.toLowerCase();
          
          if (jobTitle.includes(query) || jobLocation.includes(query)) {
              job.style.display = "block";
          } else {
              job.style.display = "none";
          }
      });
  });

  searchInput.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
          searchButton.click();
      }
  });
});

//LINKJOB PAGE

document.querySelectorAll(".job-card").forEach(card => {
  card.addEventListener("click", function() {
      window.location.href = this.getAttribute("data-url");
  });
});

// ADD POST POP-UP

function openPopup() {
    document.getElementById('addPostPopup').style.display = 'flex';
  }

  function closePopup() {
    document.getElementById('addPostPopup').style.display = 'none';
  }

  function submitPost() {
    const author = document.getElementById('postAuthor').value;
    const content = document.getElementById('postContent').value;
    const fileInput = document.getElementById('postFile').files[0];
    const postsContainer = document.getElementById('postsContainer');
    const noPostsMessage = document.getElementById('noPostsMessage');

    if (author && content) {
      const postCard = document.createElement('div');
      postCard.className = 'post-card';

      postCard.innerHTML = `
        <div class="post-header">
          <img src="https://via.placeholder.com/60" alt="Post Logo" class="post-logo">
          <div>
            <p>${author}</p>
            <span>Just now</span>
          </div>
        </div>
        <p>${content}</p>
        <img src="" alt="Post Image" class="post-image" style="display: none;">
        <div class="post-stats">
          <button onclick="toggleLike(this)" class="heart">❤</button> <span class="like-count">0 likes</span>
        </div>
        <div class="comment-section">
          <input type="text" class="comment-input" placeholder="Add a comment (username: comment)" onkeydown="addComment(event, this, '${author}')">
          <ul class="comment-list"></ul>
        </div>
      `;

      if (fileInput) {
        const reader = new FileReader();
        reader.onload = function (e) {
          const postImage = postCard.querySelector('.post-image');
          postImage.src = e.target.result;
          postImage.style.display = 'block';
        };
        reader.readAsDataURL(fileInput);
      }

      postsContainer.prepend(postCard);
      if (noPostsMessage) {
        noPostsMessage.style.display = 'none';
      }
      document.getElementById('addPostForm').reset();
      closePopup();
    } else {
      alert('Please fill in all required fields.');
    }
  }
  function toggleLike(button) {
    button.classList.toggle('liked');
    const likeCount = button.nextElementSibling;
    let count = parseInt(likeCount.textContent);
    count = button.classList.contains('liked') ? count + 1 : count - 1;
    likeCount.textContent = count;
  }

  function addComment(event, input, postAuthor) {
    if (event.key === 'Enter' && input.value.trim()) {
      const commentList = input.nextElementSibling;
      const comment = document.createElement('li');

      // Assuming the user inputs in the format: "username: comment"
      const commentText = input.value.trim();
      const [username, commentContent] = commentText.split(':').map(s => s.trim());

      if (username && commentContent) {
        comment.innerHTML = `<strong>${username}:</strong> ${commentContent}`;
      } else {
        comment.innerHTML = `<strong>${postAuthor}:</strong> ${commentText}`;
      }

      commentList.appendChild(comment);
      input.value = '';
    }
  }

// Call this function to check and display the "No posts yet" message if there are no posts
function checkNoPosts() {
    const postsContainer = document.getElementById('postsContainer');
    const noPostsMessage = document.getElementById('noPostsMessage');
  
    if (!postsContainer || !noPostsMessage) {
      console.warn("Element not found: 'postsContainer' or 'noPostsMessage' is missing.");
      return;  // Stop execution if elements are missing
    }
  
    noPostsMessage.style.display = postsContainer.children.length === 0 ? 'block' : 'none';
  }
  
// Call checkNoPosts() on page load to initialize the message
document.addEventListener('DOMContentLoaded', checkNoPosts);
  
 


document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".nav ul li a");

  links.forEach(link => {
      link.addEventListener("click", () => {
          // Highlight the active link
          links.forEach(item => item.classList.remove("active"));
          link.classList.add("active");
      });
  });

  console.log("About page script loaded successfully!");
});


//company about page edit button
//logo edit 
function editLogo() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";

    input.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const logoImg = document.querySelector(".logo-container img");
                if (logoImg) {
                    logoImg.src = e.target.result; // Update the image source
                } else {
                    alert("Logo image not found!");
                }
            };
            reader.readAsDataURL(file);
        }
    });

    input.click(); // Open file selection dialog
}

//image edit

document.addEventListener("DOMContentLoaded", function () {
    // Load saved image from localStorage
    const savedImage = localStorage.getItem("savedImage");
    if (savedImage) {
        document.querySelector(".image-container img").src = savedImage;
    }
});

function editImage() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";

    input.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const image = document.querySelector(".image-container img");
                if (image) {
                    image.src = e.target.result; // Update the image source
                } else {
                    alert("Image not found!");
                }
            };
            reader.readAsDataURL(file);
        }
    });

    input.click(); // Open file selection dialog
}

//content edit
function editMission() {
    let missionText = document.getElementById("mission-text").innerText;
    document.getElementById("mission-text").innerHTML = `
        <textarea id="mission-input" style="width: 100%;">${missionText}</textarea>
        <button class="save-btn" onclick="saveMission()">Save</button>
    `;
}

function saveMission() {
    let newMission = document.getElementById("mission-input").value;
    document.getElementById("mission-text").innerHTML = newMission;
}

function editVision() {
    let visionText = document.getElementById("vision-text").innerText;
    document.getElementById("vision-text").innerHTML = `
        <textarea id="vision-input" style="width: 100%;">${visionText}</textarea>
        <button class="save-btn" onclick="saveVision()">Save</button>
    `;
}

function saveVision() {
    let newVision = document.getElementById("vision-input").value;
    document.getElementById("vision-text").innerHTML = newVision;
}

function editValues() {
    let valuesList = document.getElementById("values-list");
    let listItems = valuesList.getElementsByTagName("li");

    // Convert list items to a single text block
    let valuesText = Array.from(listItems).map(li => li.innerText).join("\n");

    // Replace list with textarea (keeps structure intact)
    valuesList.innerHTML = `
        <textarea id="values-input" style="width: 100%; height: 80px;">${valuesText}</textarea>
        <button class="save-btn" onclick="saveValues()">Save</button>
    `;
}

function saveValues() {
    let valuesInput = document.getElementById("values-input").value;

    // Convert back into list items
    let newValuesList = valuesInput.split("\n")
        .map(value => value.trim()) // Remove extra spaces
        .filter(value => value !== "") // Remove empty lines
        .map(value => `<li>${value}</li>`) // Convert to list items
        .join("");

    document.getElementById("values-list").innerHTML = newValuesList;
}

//footer edit
document.addEventListener("DOMContentLoaded", function () {
    const footerText = document.getElementById("footer-text");
    const footerEditBtn = document.getElementById("footer-edit-btn");

    document.addEventListener("DOMContentLoaded", function () {
        const someElement = document.getElementById('someElementID');
        if (someElement) {
          someElement.addEventListener("click", function () {
            console.log("Element clicked!");
          });
        } else {
          console.warn("Element with ID 'someElementID' not found.");
        }
      });
      
});




//add job card


document.addEventListener("DOMContentLoaded", function () {
    const openFormBtn = document.getElementById("openJobForm");
    const closeFormBtn = document.getElementById("closeJobForm");
    const jobForm = document.getElementById("jobForm");
    const submitJobBtn = document.getElementById("submitJob");

    const jobTitleInput = document.getElementById("jobTitle");
    const companyNameInput = document.getElementById("companyName");
    const locationInput = document.getElementById("location");
    const datePostedInput = document.getElementById("datePosted");

    const recommendedJobs = document.querySelector(".job-cards");

    // Show the job form
    openFormBtn.addEventListener("click", function () {
        jobForm.style.display = "block";
    });

    // Hide the job form
    closeFormBtn.addEventListener("click", function () {
        jobForm.style.display = "none";
    });

    // Add job on form submit
    submitJobBtn.addEventListener("click", function () {
        const jobTitle = jobTitleInput.value.trim();
        const companyName = companyNameInput.value.trim();
        const location = locationInput.value.trim();
        const datePosted = datePostedInput.value.trim();

        if (!jobTitle || !companyName || !location || !datePosted) {
            alert("Please fill in all fields!");
            return;
        }

        // Create new job card
        const jobCard = document.createElement("div");
        jobCard.classList.add("job-card");

        jobCard.innerHTML = `
            <img src="https://cdn.iconscout.com/icon/free/png-256/microsoft-47-722716.png" alt="Company Logo">
            <h4>${jobTitle}</h4>
            <p>${companyName}</p>
            <p>${location}</p>
            <span class="date">${datePosted}</span>
            <button class="delete-job btn btn-danger">Delete</button>
        `;

        recommendedJobs.appendChild(jobCard);

        // Clear form inputs
        jobTitleInput.value = "";
        companyNameInput.value = "";
        locationInput.value = "";
        datePostedInput.value = "";

        // Close form
        jobForm.style.display = "none";

        // Add delete function to remove job card
        jobCard.querySelector(".delete-job").addEventListener("click", function () {
            recommendedJobs.removeChild(jobCard);
        });
    });
});

