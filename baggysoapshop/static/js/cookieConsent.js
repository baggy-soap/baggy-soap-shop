
// GDPR consent function checks and writes cookies to browser.
const cookieStorage = {
    getItem: (key) =>{
        const cookies = document.cookie
            .split(';')
            .map(cookie => cookie.split('='))
            .reduce((acc, [key, value]) => ({ ...acc, [key.trim()]: value }), {});
        return cookies[key]
    },
    setItem: (key, value) =>{
        var d = new Date();
        d.setTime(d.getTime() + (100 * 24 * 60 * 60 * 1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = key + "=" + value + ";" + expires + ";path=/";
    },
};

const consentPropertyName = 'Baggy_soap_shop_gdpr_consent';
const shouldShowPopup = () => !cookieStorage.getItem(consentPropertyName);
const saveToStorage = () => cookieStorage.setItem(consentPropertyName, true);
  
window.onload = () =>{
      const consentPopup = document.getElementById('consent-popup');
      const acceptBtn = document.getElementById('accept');
  
      const acceptEvent = event => {
          saveToStorage(cookieStorage);
          consentPopup.classList.add('hidden');
      };
  
      acceptBtn.addEventListener('click', acceptEvent);
  
      if (shouldShowPopup()) {
          // waits 800ms before showing the modal.
          setTimeout(() => {
             consentPopup.classList.remove('hidden'); 
          }, 500);
      }
};