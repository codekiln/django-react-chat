
/**
 * Given an array or a list of options, return only the
 * items that are Some(item)
 **/
let arr_only_some = (arr) => Array.fold_right(
    (x, result) =>
      switch x {
      | Some(i) => Array.append([|i|], result)
      | None => result
      },
  	arr,
    [||]
  );

let ste = ReasonReact.stringToElement
