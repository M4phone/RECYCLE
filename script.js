document.addEventListener('DOMContentLoaded', function () {
    // Initialize AOS Animation Library
    AOS.init({
        duration: 800,
        once: true,
        offset: 100
    });

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Close all other items
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
            });

            // Toggle current item
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Google Sheets Integration
    // TODO: 사용자가 배포 후 생성된 URL을 아래에 입력해야 합니다.
    const GOOGLE_SCRIPT_URL = "YOUR_GOOGLE_SCRIPT_WEB_APP_URL_HERE"; 

    const quoteForm = document.getElementById('quoteForm');
    if (quoteForm) {
        quoteForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerText;
            
            // 입력 값 가져오기
            const company = this.querySelector('input[placeholder="예: 폰리사이클"]').value;
            const name = this.querySelector('input[placeholder="홍길동"]').value;
            const phone = this.querySelector('input[placeholder="010-0000-0000"]').value;
            const message = this.querySelector('textarea').value;

            if (!company || !name || !phone) {
                alert('필수 정보를 모두 입력해주세요.');
                return;
            }

            // 로딩 상태 표시
            submitBtn.innerText = '전송 중...';
            submitBtn.disabled = true;

            fetch(GOOGLE_SCRIPT_URL, {
                method: 'POST',
                mode: 'no-cors', // Google Apps Script는 no-cors 모드로 요청해야 함
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    company: company,
                    name: name,
                    phone: phone,
                    message: message
                })
            })
            .then(response => {
                // no-cors 모드에서는 response를 읽을 수 없지만, 에러가 안 나면 성공으로 간주
                alert('견적 요청이 성공적으로 전송되었습니다. 담당자가 곧 연락드리겠습니다.');
                quoteForm.reset();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
            })
            .finally(() => {
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;
            });
        });
    }

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
