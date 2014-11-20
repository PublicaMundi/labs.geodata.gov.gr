export CATALINA_OPTS="-server -Xmsi1224M -Xmx1524M -XX:+UseParallelGC -XX:SoftRefLRUPolicyMSPerMB=36000 -XX:MaxPermSize=128m"
su - tomcat -c /home/tomcat/tomcat1/bin/startup.sh
