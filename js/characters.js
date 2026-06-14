  // nav: scrolled border + mobile toggle
  var nav=document.getElementById('nav');
  addEventListener('scroll',function(){nav.classList.toggle('scrolled',scrollY>8);},{passive:true});
  var t=document.getElementById('navToggle'),l=document.getElementById('navLinks');
  t.addEventListener('click',function(){var o=l.classList.toggle('open');t.setAttribute('aria-expanded',o);document.body.classList.toggle('nav-open',o);});
  [].slice.call(l.querySelectorAll('a')).forEach(function(a){a.addEventListener('click',function(){
    l.classList.remove('open');t.setAttribute('aria-expanded','false');document.body.classList.remove('nav-open');});});
  document.getElementById('yr').textContent=new Date().getFullYear();
</script>

  (function () {
    var btn = document.getElementById('poem-say');
    if (!btn) return;
    var audio = null;
    btn.addEventListener('click', function () {
      if (audio && !audio.paused) {
        audio.pause();
        audio.currentTime = 0;
        btn.classList.remove('is-speaking');
        audio = null;
        return;
      }
      audio = new Audio('learn/audio/poem-yonge.mp3');
      btn.classList.add('is-speaking');
      audio.onended = audio.onerror = function () {
        btn.classList.remove('is-speaking');
        audio = null;
      };
      audio.play();
    });
  })();
