document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('nav');
    const navLinks = document.querySelector('.nav-links');

    burger.addEventListener('click', () => {
        nav.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            nav.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    const initHeaderSlider = () => {
        const sliderDots = document.querySelectorAll('.slider-dot');
        const slides = document.querySelectorAll('.square img');
        let currentSlide = 0;
        let slideInterval;
        let isAnimating = false;

        const showSlide = (index) => {
            if (isAnimating) return;
            isAnimating = true;

            slides[currentSlide].style.opacity = '0';
            sliderDots[currentSlide].classList.remove('active');

            setTimeout(() => {
                slides[currentSlide].style.display = 'none';
                slides[index].style.display = 'block';
                
                setTimeout(() => {
                    slides[index].style.opacity = '1';
                    sliderDots[index].classList.add('active');
                    currentSlide = index;
                    isAnimating = false;
                }, 50);
            }, 500);
        };

        const nextSlide = () => {
            const next = (currentSlide + 1) % slides.length;
            showSlide(next);
        };

        const startAutoSlide = () => {
            slideInterval = setInterval(nextSlide, 5000);
        };

        const stopAutoSlide = () => {
            clearInterval(slideInterval);
        };

        sliderDots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                if (currentSlide === index || isAnimating) return;
                stopAutoSlide();
                showSlide(index);
                startAutoSlide();
            });
        });

        startAutoSlide();
    };

    const initPortfolioSlider = () => {
        const textSlides = document.querySelectorAll('.text-slide');
        const imageSlides = document.querySelectorAll('.image-slide');
        const dots = document.querySelectorAll('.portfolio-dot');
        const prevButton = document.querySelector('.prev-slide');
        const nextButton = document.querySelector('.next-slide');
        let currentSlide = 0;
        let isAnimating = false;

        const showSlide = (index) => {
            if (isAnimating) return;
            isAnimating = true;

            textSlides[currentSlide].classList.remove('active');
            imageSlides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');

            textSlides[index].classList.add('active');
            imageSlides[index].classList.add('active');
            dots[index].classList.add('active');

            currentSlide = index;

            setTimeout(() => {
                isAnimating = false;
            }, 500);
        };

        const nextSlide = () => {
            const next = (currentSlide + 1) % textSlides.length;
            showSlide(next);
        };

        const prevSlide = () => {
            const prev = (currentSlide - 1 + textSlides.length) % textSlides.length;
            showSlide(prev);
        };

        prevButton.addEventListener('click', prevSlide);
        nextButton.addEventListener('click', nextSlide);

        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                if (currentSlide !== index && !isAnimating) {
                    showSlide(index);
                }
            });
        });
    };

    initHeaderSlider();
    initPortfolioSlider();

    console.log('DOM fully loaded');

    const form = document.getElementById('appForm');
    if (!form) {
        console.error('Form with ID "appForm" not found');
        return;
    }

    console.log('Form found, attaching event listener');

    form.addEventListener('submit', async (e) => {
        console.log('Form submit event triggered');
        e.preventDefault();

        const formData = new FormData(form);
        const resultDiv = document.getElementById('result');
        const overlay = document.getElementById('overlay');

        if (!resultDiv || !overlay) {
            console.error('Result div or overlay not found');
            return;
        }

        overlay.style.display = 'block';
        resultDiv.style.display = 'block';
        
        setTimeout(() => {
            overlay.classList.add('active');
            resultDiv.classList.add('active');
        }, 10);

        try {
            console.log('Sending fetch request to /submit');
            const response = await fetch('/submit', {
                method: 'POST',
                body: formData
            });

            console.log('Response received', response);
            const data = await response.json();
            console.log('Parsed data', data);

            if (response.ok) {
                resultDiv.className = 'modal active success';
                resultDiv.innerHTML = `
                    <p>${data.message}</p>
                    <button class="close-btn">Закрыть</button>
                `;
                form.reset();
            } else {
                resultDiv.className = 'modal active error';
                const messages = data.message.split('; ').map(msg => msg.split(': ')[1] || msg).filter(Boolean);
                resultDiv.innerHTML = `
                    <p>${messages.join('<br>')}</p>
                    <button class="close-btn">Закрыть</button>
                `;
            }
        } catch (error) {
            console.error('Fetch error', error);
            resultDiv.className = 'modal active error';
            resultDiv.innerHTML = `
                <p>Ошибка соединения с сервером</p>
                <button class="close-btn">Закрыть</button>
            `;
        }

        const closeBtn = resultDiv.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.onclick = () => {
                overlay.classList.remove('active');
                resultDiv.classList.remove('active');
                
                setTimeout(() => {
                    resultDiv.style.display = 'none';
                    overlay.style.display = 'none';
                    resultDiv.innerHTML = '';
                    resultDiv.className = 'modal';
                }, 300);
            };
        }
    });
});