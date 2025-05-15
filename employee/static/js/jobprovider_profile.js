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
          <button onclick="toggleLike(this)" class="heart">❤</button> <span class="like-count">0</span>
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

  if (postsContainer.children.length === 0) {
    noPostsMessage.style.display = 'block';
  } else {
    noPostsMessage.style.display = 'none';
  }
}

// Call checkNoPosts() on page load to initialize the message
document.addEventListener('DOMContentLoaded', checkNoPosts);
  
 

// ABOUT PAGE

  // Navigation Scroll Behavior
//document.querySelectorAll('.nav-link').forEach(link => {
  //link.addEventListener('click', (e) => {
    //  e.preventDefault();
      //const targetId = e.target.getAttribute('href').slice(1);
      //const targetSection = document.getElementById(targetId);
      
      //if (targetSection) {
        //  window.scrollTo({
          //    top: targetSection.offsetTop - 50,
            //  behavior: 'smooth'
          //});
      //}
  //});
//});

// Footer Year Update (Optional Dynamic Year)
//const footer = document.querySelector('.footer p');
//const currentYear = new Date().getFullYear();
//footer.innerHTML = `&copy; ${currentYear} Business Name. All rights reserved.`;

// Example functionality for interactivity (optional)
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
