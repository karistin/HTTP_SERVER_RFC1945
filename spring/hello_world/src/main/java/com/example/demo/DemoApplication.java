package com.example.demo;

import com.example.demo.domain.Task;
import com.example.demo.repository.TaskMemoryRepository;
import com.example.demo.repository.TaskRepository;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		TaskRepository taskRepository = new TaskMemoryRepository();
		Task task = new Task();
		task.setTitle("ksj");
		task.setContents("1q2w3e");
		Task task2 = new Task();
		task2.setTitle("lavius");
		task2.setContents("lavius123");
		taskRepository.save(task);
		taskRepository.save(task2);

		SpringApplication.run(DemoApplication.class, args);
	}

}
