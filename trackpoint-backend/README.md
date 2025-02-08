>> 记录一些心得、技巧、遇到的问题和解决方法


1. redis+布隆过滤器的Docker镜像`redislabs/rebloom:latest`，包含redis基本镜像及布隆过滤器功能;
2. `requirements.txt`中库的版本一定要和本地开发时严格对应，不然指不定报什么错；
3. docker中指定初始化数据的数据卷时，里面的中文乱码，解决：`.sql`前面加`/*!40101 SET NAMES utf8 */;`；