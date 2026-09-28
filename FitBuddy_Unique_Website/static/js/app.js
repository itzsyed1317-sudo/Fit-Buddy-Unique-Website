function showLoading(form){
  form.classList.add("loading");
  const button=form.querySelector("button");
  if(button) button.disabled=true;
}
document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll("input,textarea").forEach(el=>{
    el.addEventListener("keydown",e=>{ if(e.key==="Enter" && el.tagName==="TEXTAREA") e.stopPropagation(); });
  });
});
