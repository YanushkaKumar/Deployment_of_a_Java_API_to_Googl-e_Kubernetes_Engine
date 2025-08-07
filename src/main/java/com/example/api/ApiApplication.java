package com.example.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.*;

@SpringBootApplication
@RestController
public class ApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiApplication.class, args);
	}

	@GetMapping("/health")
	public Map<String, String> health() {
		Map<String, String> response = new HashMap<>();
		response.put("status", "UP");
		response.put("timestamp", new Date().toString());
		return response;
	}

	@GetMapping("/api/users")
	public List<Map<String, Object>> getUsers() {
		return Arrays.asList(
				Map.of("id", 1, "name", "John Doe", "email", "john@example.com"),
				Map.of("id", 2, "name", "Jane Smith", "email", "jane@example.com")
		);
	}
}
