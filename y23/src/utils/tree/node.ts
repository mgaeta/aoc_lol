enum SearchMode {
    DEPTH_FIRST = "depth_first",
    BREADTH_FIRST = "breadth_first",
}

class TreeNode<T> {
    parent?: TreeNode<T>;
    children: TreeNode<T>[];
    value: T;
    name: string;

    constructor(value: T, name?: string) {
        this.children = [];
        this.value = value;
        // TODO maybe this should be a UUID
        this.name = name || `${value}`;
    }

    addChild(child: TreeNode<T>): void {
        child.parent = this;
        this.children.push(child);
    }

    find(name: string, options?: {
        debug?: boolean
        mode?: string,
    }): TreeNode<T> | undefined {
        if (this.name === name) return this;

        if (options?.mode === SearchMode.BREADTH_FIRST) {
            const queue: TreeNode<T>[] = [this];
            while (true) {
                const next = queue.shift();
                if (!next) break;
                if (next.name === name) return next;
                queue.push(...next.children);
            }
            return undefined;
        }

        for (const child of this.children) {
            const found = child.find(name, options);
            if (found) return found;
        }
        return undefined;
    }

    getAncestors(): TreeNode<T>[] {
        if (!this.parent) return [];
        const ancestors = this.parent.getAncestors();
        ancestors.push(this.parent);
        return ancestors;
    }

    firstCommonAncestor(other: TreeNode<T>, options?: {
        debug?: boolean
    }): TreeNode<T> {
        const ancestorsNames = new Set<string>(this.getAncestors().map(i => i.name));

        let parent: TreeNode<T> | undefined = other;
        while (parent) {
            if (ancestorsNames.has(parent.name)) return parent;
            parent = parent.parent;
        }
        throw new Error("invalid trees");
    }

}
