// Image Enhancer App
document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const originalImg = document.getElementById('originalImg');
    const originalPlaceholder = document.getElementById('originalPlaceholder');
    const enhancedImg = document.getElementById('enhancedImg');
    const enhancedPlaceholder = document.getElementById('enhancedPlaceholder');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const algorithmSelect = document.getElementById('algorithmSelect');
    const gammaSlider = document.getElementById('gammaSlider');
    const gammaValue = document.getElementById('gammaValue');
    const applyBtn = document.getElementById('applyBtn');
    const uploadPreview = document.getElementById('uploadPreview');
    const gammaControls = document.getElementById('gammaControls');
    
    let currentImageFile = null;
    
    // Toggle gamma controls
    algorithmSelect.addEventListener('change', function() {
        if (this.value === 'gamma') {
            gammaControls.style.display = 'block';
        } else {
            gammaControls.style.display = 'none';
        }
    });
    
    // Gamma slider realtime update
    gammaSlider.addEventListener('input', function() {
        gammaValue.textContent = this.value;
        if (currentImageFile && this.value) {
            applyEnhancement(); // Realtime preview
        }
    });
    
    // Update gamma value display
    gammaValue.textContent = gammaSlider.value;
    
    // Image upload
    imageUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
            currentImageFile = file;
            
            // Preview in sidebar
            const reader = new FileReader();
            reader.onload = function(e) {
                uploadPreview.innerHTML = `<img src="${e.target.result}" class="img-thumbnail">`;
            };
            reader.readAsDataURL(file);
            
            // Show original in main area
            const originalReader = new FileReader();
            originalReader.onload = function(e) {
                originalImg.src = e.target.result;
                originalImg.style.display = 'block';
                originalPlaceholder.style.display = 'none';
                enhancedImg.style.display = 'none';
                enhancedPlaceholder.style.display = 'block';
                applyBtn.disabled = false;
            };
            originalReader.readAsDataURL(file);
        } else {
            alert('Please select a valid JPG or PNG image.');
            currentImageFile = null;
        }
    });

    // Apply enhancement
    applyBtn.addEventListener('click', applyEnhancement);
    
    async function applyEnhancement() {
        if (!currentImageFile) return;
        
        loadingSpinner.style.display = 'block';
        enhancedImg.style.display = 'none';
        enhancedPlaceholder.style.display = 'none';
        applyBtn.disabled = true;
        
        const formData = new FormData();
        formData.append('image', currentImageFile);
        formData.append('algorithm', algorithmSelect.value);
        formData.append('gamma', gammaSlider.value);
        
        try {
            const response = await fetch('/api/enhance/', {
                method: 'POST',
                body: formData,
            });
            
            const data = await response.json();
            
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                enhancedImg.src = data.image;
                enhancedImg.style.display = 'block';
                enhancedPlaceholder.style.display = 'none';
            }
        } catch (error) {
            alert('Request failed: ' + error.message);
        } finally {
            loadingSpinner.style.display = 'none';
            applyBtn.disabled = false;
        }
    }
});

