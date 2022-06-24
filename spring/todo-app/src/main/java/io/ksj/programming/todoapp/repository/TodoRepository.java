package io.ksj.programming.todoapp.repository;

import io.ksj.programming.todoapp.entity.Todo;
import io.ksj.programming.todoapp.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TodoRepository extends JpaRepository<Todo, Long>{
}
