package com.example.demo.controller;

import com.example.demo.domain.Task;
import com.example.demo.repository.TaskMemoryRepository;
import com.example.demo.repository.TaskRepository;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/tasks")
public class GreetingController {
    TaskRepository taskRepository = new TaskMemoryRepository();


    @GetMapping()
    public ResponseEntity GetApi(){
        return ResponseEntity.ok()
                .body(taskRepository.findAll());
    }

    @GetMapping(path = "{taskId}")
    public ResponseEntity GetApi(@PathVariable(name = "taskId") Long taskId){
        if (taskRepository.findId(taskId).isPresent())
        {
            return ResponseEntity.ok()
                    .body(taskRepository.findId(taskId));
        }else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @PostMapping()
    public ResponseEntity PostApi(@RequestBody HashMap<String, String> map){
        Task task = new Task();
        task.setTitle(map.get("title"));
        task.setContents(map.get("contents"));
        taskRepository.save(task);
        return ResponseEntity.ok()
                .body(task.getTaskId());
    }
    @PostMapping(path = "{taskId}")
    public ResponseEntity PostApi(@PathVariable(name = "taskId") Long taskId,@RequestBody HashMap<String, String> map){
        Task task = new Task();
        task.setTitle(map.get("title"));
        task.setContents(map.get("contents"));
        if (taskRepository.amendTask(taskId, task))
        {
            return new ResponseEntity<>(HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    @DeleteMapping(path = "{taskId}")
    public ResponseEntity DeleteApi(@PathVariable(name = "taskId") Long taskId){
        if (taskRepository.deleteId(taskId))
        {
            return new ResponseEntity<>(HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    @GetMapping("/test")
    public ResponseEntity<String> test(){
        HttpHeaders responseHeaders = new HttpHeaders();
        responseHeaders.set("Baeldung-Example-Header", "Value-ResponseEntityBuilderWithHttpHeaders");

        return ResponseEntity.ok()
                .header(String.valueOf(responseHeaders))
                .body("Response with header using ResponseEntity");
    }

}

