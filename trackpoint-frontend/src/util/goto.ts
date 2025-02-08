/**
 * 定时跳转到控制台
 * @param delay 
 */
export function goToDashBoard(delay: number = 0) {
    // 后面多出来一个'/'，就会定位到dashboard目录下的index.html，打开新页面，url不显示index.html
    // 如果不写，会跳到该路由，该路由又调用这个函数，造成无限循环
    setTimeout(() => { window.open('../../dashboard/', '_self') }, delay)
}


/**
 * 跳转到公共页面
 */
export function goToPublicPage(delay: number = 0) {
    setTimeout(() => { window.open('../../', '_self') }, delay)

}