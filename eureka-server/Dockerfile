FROM maven:3-openjdk-11 AS MAVEN_BUILD
MAINTAINER Marco Yuquilima
COPY pom.xml /build/
COPY src /build/src/
WORKDIR /build/
RUN mvn package
FROM openjdk:11
WORKDIR /app
EXPOSE 8761
COPY --from=MAVEN_BUILD /build/target/eureka-server-0.0.1-SNAPSHOT.jar /app/
ENTRYPOINT ["java", "-jar", "eureka-server-0.0.1-SNAPSHOT.jar"]