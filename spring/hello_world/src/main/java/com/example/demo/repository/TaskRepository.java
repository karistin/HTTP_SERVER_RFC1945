package com.example.demo.repository;

import com.example.demo.domain.Task;

import java.util.List;
import java.util.Optional;

public interface TaskRepository {
    Task save(Task task);
    Optional <Task> findId(Long id);
    List<Task> findAll();
    boolean deleteId(Long id);
    boolean amendTask(Long id, Task task);
}
